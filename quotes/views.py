from django.db.models import F, Sum, Count
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Quote, Source
from .forms import QuoteForm


def home(request: HttpRequest) -> HttpResponse:
    quote = Quote.objects.random_weighted()
    context = {"quote": quote}

    if quote:
        Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
        quote.views += 1

    return render(request, "quotes/home.html", context)


def like(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    get_object_or_404(Quote, pk=pk)
    Quote.objects.filter(pk=pk).update(likes=F("likes") + 1)
    return redirect("quotes:home")


def dislike(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    get_object_or_404(Quote, pk=pk)
    Quote.objects.filter(pk=pk).update(dislikes=F("dislikes") + 1)
    return redirect("quotes:home")


def add_quote(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Цитата добавлена.")
            return redirect("quotes:home")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def top10(request: HttpRequest) -> HttpResponse:
    qs = Quote.objects.select_related("source")

    type_val = request.GET.get("type") or ""
    source_id = request.GET.get("source") or ""

    if type_val:
        qs = qs.filter(source__type=type_val)
    if source_id:
        qs = qs.filter(source_id=source_id)

    top_quotes = qs.order_by("-likes", "-views", "-created_at")[:10]

    totals = Quote.objects.aggregate(
        total_quotes=Count("id"),
        total_sources=Count("source", distinct=True),
        total_likes=Sum("likes"),
        total_dislikes=Sum("dislikes"),
        total_views=Sum("views"),
    )

    sources = Source.objects.order_by("name").all()
    types = (
        Source.objects.exclude(type="")
        .values_list("type", flat=True)
        .distinct()
        .order_by("type")
    )

    context = {
        "quotes": top_quotes,
        "filters": {"type": type_val, "source": source_id},
        "sources": sources,
        "types": types,
        "totals": totals,
    }
    return render(request, "quotes/top.html", context)
