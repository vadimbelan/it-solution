from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["source", "text", "weight"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "source": forms.Select(attrs={"class": "form-select"}),
        }
