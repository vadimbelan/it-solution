from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["source", "text", "weight"]
        widgets = {
            "source": forms.Select(attrs={"class": "form-select"}),
            "text": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "weight": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        if not cleaned:
            return cleaned
        instance = Quote(
            source=cleaned.get("source"),
            text=cleaned.get("text") or "",
            weight=cleaned.get("weight") or 1,
        )
        instance.full_clean()
        return cleaned
