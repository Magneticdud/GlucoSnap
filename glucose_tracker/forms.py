from django import forms
from .models import GlucoseReading, Meal
from django.utils.translation import gettext_lazy as _


class GlucoseReadingForm(forms.ModelForm):
    class Meta:
        model = GlucoseReading
        fields = ["glucose_level", "measurement_type", "timestamp", "notes"]
        widgets = {
            "timestamp": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "glucose_level": forms.NumberInput(
                attrs={"class": "form-control", "min": 20, "max": 600}
            ),
            "measurement_type": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_glucose_level(self):
        level = self.cleaned_data.get("glucose_level")
        if level < 20 or level > 600:
            raise forms.ValidationError(
                _("Glucose level must be between 20 and 600 mg/dL.")
            )
        return level


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["photo", "meal_type", "timestamp", "manual_notes"]
        widgets = {
            "timestamp": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "meal_type": forms.Select(attrs={"class": "form-select"}),
            "manual_notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "photo": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }
