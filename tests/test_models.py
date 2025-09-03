import pytest
from django.core.exceptions import ValidationError

from quotes.models import Source, Quote


@pytest.mark.django_db
def test_max_three_quotes_per_source():
    src = Source.objects.create(name="Тестовый источник", type="фильм")
    Quote.objects.create(source=src, text="цитата 1", weight=1)
    Quote.objects.create(source=src, text="цитата 2", weight=1)
    Quote.objects.create(source=src, text="цитата 3", weight=1)

    q4 = Quote(source=src, text="цитата 4", weight=1)
    with pytest.raises(ValidationError):
        q4.full_clean()


@pytest.mark.django_db
def test_unique_text():
    src = Source.objects.create(name="Источник", type="книга")
    Quote.objects.create(source=src, text="уникальный текст", weight=1)
    dup = Quote(source=src, text="уникальный текст", weight=1)
    with pytest.raises(ValidationError):
        dup.full_clean()


@pytest.mark.django_db
def test_weighted_random_selection_monkeypatch(monkeypatch):
    src = Source.objects.create(name="Источник", type="фильм")
    q1 = Quote.objects.create(source=src, text="а", weight=1)
    q2 = Quote.objects.create(source=src, text="б", weight=3)

    monkeypatch.setattr("quotes.models.randint", lambda a, b: 1)
    assert Quote.objects.random_weighted().id == q1.id

    monkeypatch.setattr("quotes.models.randint", lambda a, b: 2)
    assert Quote.objects.random_weighted().id == q2.id

    monkeypatch.setattr("quotes.models.randint", lambda a, b: 4)
    assert Quote.objects.random_weighted().id == q2.id
