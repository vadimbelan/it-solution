from django.db import transaction
from django.db.models import F, Sum, Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import QuoteForm
from .models import Quote, Source


def home(request):
    quote = Quote.objects.random_weighted()
    if quote:
        Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
        quote.refresh_from_db(fields=["views"])
    context = {"quote": quote}
    return render(request, "quotes/home.html", context)


def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:home")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def like(request, pk: int):
    if request.method != "POST":
        raise Http404
    Quote.objects.filter(pk=pk).update(likes=F("likes") + 1)
    return HttpResponseRedirect(reverse("quotes:home"))


def dislike(request, pk: int):
    if request.method != "POST":
        raise Http404
    Quote.objects.filter(pk=pk).update(dislikes=F("dislikes") + 1)
    return HttpResponseRedirect(reverse("quotes:home"))


def top_quotes(request):
    source_id = request.GET.get("source")
    source_type = request.GET.get("type")

    qs = Quote.objects.select_related("source").order_by("-likes", "-views", "-created_at")
    if source_id:
        qs = qs.filter(source_id=source_id)
    if source_type:
        qs = qs.filter(source__type=source_type)

    top_list = list(qs[:10])
    sources = Source.objects.order_by("name")
    types = Source.objects.exclude(type="").values_list("type", flat=True).distinct().order_by("type")

    return render(
        request,
        "quotes/top.html",
        {
            "quotes": top_list,
            "sources": sources,
            "types": types,
            "selected_source": int(source_id) if source_id else None,
            "selected_type": source_type or "",
        },
    )


def dashboard(request):
    total_sources = Source.objects.count()
    total_quotes = Quote.objects.count()

    aggregates = Quote.objects.aggregate(
        likes_sum=Sum("likes"),
        dislikes_sum=Sum("dislikes"),
        views_sum=Sum("views"),
        weight_sum=Sum("weight"),
    )
    likes_sum = aggregates.get("likes_sum") or 0
    dislikes_sum = aggregates.get("dislikes_sum") or 0
    views_sum = aggregates.get("views_sum") or 0
    weight_sum = aggregates.get("weight_sum") or 0

    top_sources_by_likes = (
        Source.objects.annotate(total_likes=Sum("quotes__likes"))
        .order_by("-total_likes", "name")
        .values("id", "name", "type", "total_likes")[:5]
    )

    top_quotes_by_views = (
        Quote.objects.select_related("source")
        .order_by("-views", "-likes", "-created_at")
        .values("id", "text", "views", "likes", "dislikes", "source__name")[:5]
    )

    # распределение по весам (сколько цитат каждого веса)
    weight_distribution = (
        Quote.objects.values("weight").annotate(cnt=Count("id")).order_by("weight")
    )

    context = {
        "total_sources": total_sources,
        "total_quotes": total_quotes,
        "likes_sum": likes_sum,
        "dislikes_sum": dislikes_sum,
        "views_sum": views_sum,
        "weight_sum": weight_sum,
        "top_sources_by_likes": top_sources_by_likes,
        "top_quotes_by_views": top_quotes_by_views,
        "weight_distribution": weight_distribution,
    }
    return render(request, "quotes/dashboard.html", context)
