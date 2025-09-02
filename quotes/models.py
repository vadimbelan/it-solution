from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        if self.type:
            return f"{self.name} ({self.type})"
        return self.name


class Quote(models.Model):
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name="quotes",
    )
    text = models.TextField(unique=True)
    weight = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.text[:60]

    def clean(self):
        super().clean()
        if not self.source_id:
            return
        qs = Quote.objects.filter(source_id=self.source_id)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.count() >= 3:
            raise ValidationError(
                {"source": "У одного источника может быть не более 3 цитат."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
