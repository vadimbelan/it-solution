import pytest
from django.urls import reverse
from django.db.models import F

from quotes.models import Source, Quote


@pytest.mark.django_db
def test_home_without_quotes(client):
    resp = client.get(reverse("quotes:home"))
    assert resp.status_code == 200
    assert "Пока нет цитат" in resp.content.decode("utf-8")


@pytest.mark.django_db
def test_home_with_quote_increments_views(client):
    src = Source.objects.create(name="Источник", type="фильм")
    q = Quote.objects.create(source=src, text="привет", weight=1, views=0)
    resp = client.get(reverse("quotes:home"))
    assert resp.status_code == 200
    q.refresh_from_db()
    assert q.views == 1


@pytest.mark.django_db
def test_like_and_dislike_endpoints(client):
    src = Source.objects.create(name="Источник", type="фильм")
    q = Quote.objects.create(source=src, text="текст", weight=1)

    resp = client.post(reverse("quotes:like", args=[q.id]))
    assert resp.status_code == 302
    q.refresh_from_db()
    assert q.likes == 1

    resp = client.post(reverse("quotes:dislike", args=[q.id]))
    assert resp.status_code == 302
    q.refresh_from_db()
    assert q.dislikes == 1


@pytest.mark.django_db
def test_top_page_and_filters(client):
    s1 = Source.objects.create(name="Матрица", type="фильм")
    s2 = Source.objects.create(name="Дюна", type="книга")
    Quote.objects.create(source=s1, text="а", weight=1, likes=5)
    Quote.objects.create(source=s2, text="б", weight=1, likes=1)

    resp = client.get(reverse("quotes:top"))
    assert resp.status_code == 200
    html = resp.content.decode("utf-8")
    assert "Топ-10 по лайкам" in html
    assert "Матрица" in html

    resp = client.get(reverse("quotes:top"), {"source": s2.id})
    assert resp.status_code == 200
    html = resp.content.decode("utf-8")
    assert "Дюна" in html
    assert f'value="{s2.id}" selected' in html


@pytest.mark.django_db
def test_dashboard_page(client):
    s = Source.objects.create(name="Источник X", type="фильм")
    Quote.objects.create(source=s, text="цитата 1", weight=1, views=2, likes=1)
    Quote.objects.create(source=s, text="цитата 2", weight=3, views=5, likes=4)

    resp = client.get(reverse("quotes:dashboard"))
    assert resp.status_code == 200
    html = resp.content.decode("utf-8")
    assert "Дашборд" in html
    assert "Топ источников по лайкам" in html
    assert "Распределение по весам" in html
