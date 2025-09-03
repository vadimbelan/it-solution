from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_quote, name="add"),
    path("top/", views.top_quotes, name="top"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("like/<int:pk>/", views.like, name="like"),
    path("dislike/<int:pk>/", views.dislike, name="dislike"),
]
