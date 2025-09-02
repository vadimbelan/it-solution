from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.home, name="home"),
    path("like/<int:pk>/", views.like, name="like"),
    path("dislike/<int:pk>/", views.dislike, name="dislike"),
    path("add/", views.add_quote, name="add"),
]
