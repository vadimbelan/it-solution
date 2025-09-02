from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Quote


def home(request: HttpRequest) -> HttpResponse:
    quote = Quote.objects.random_weighted()
    context = {"quote": quote}

    if quote:
        Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
        quote.views += 1

    return render(request, "quotes/home.html", context)
