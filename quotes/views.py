from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Quote
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
            quote = form.save()
            messages.success(request, "Цитата добавлена.")
            return redirect("quotes:home")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})
