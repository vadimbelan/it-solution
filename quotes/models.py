from random import randint

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


class Source(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64, blank=True, default="")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class QuoteManager(models.Manager):
    def random_weighted(self):
        qs = self.get_queryset().only("id", "weight").order_by("id")
        values = list(qs.values_list("id", "weight"))
        if not values:
            return None

        total = sum(w for _, w in values)
        if total <= 0:
            return self.get_queryset().first()

        r = randint(1, total)

        cumulative = 0
        picked_id = None
        for obj_id, weight in values:
            cumulative += int(weight)
            if r <= cumulative:
                picked_id = obj_id
                break

        if picked_id is None:
            # теоретически не должно случиться, но на всякий случай
            picked_id = values[-1][0]
        return self.get_queryset().select_related("source").get(pk=picked_id)


class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="quotes")
    text = models.TextField(unique=True)
    weight = models.PositiveIntegerField(default=1)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuoteManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.text[:30]}..."

    def clean(self):
        # Ограничение: не более 3 цитат на источник
        if self.source_id:
            qs = Quote.objects.filter(source_id=self.source_id)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            count = qs.count()
            if count >= 3:
                raise ValidationError("У одного источника может быть не более 3 цитат.")

        # Дополнительно: вес должен быть >=1
        if self.weight <= 0:
            raise ValidationError({"weight": "Вес должен быть положительным."})
