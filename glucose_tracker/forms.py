from django import forms
from .models import GlucoseReading, Meal, MeasurementSchedule

class MeasurementScheduleForm(forms.ModelForm):
    class Meta:
        model = MeasurementSchedule
        fields = [
            # Monday
            "mon_pre_breakfast", "mon_post_breakfast", "mon_pre_lunch", "mon_post_lunch",
            "mon_pre_dinner", "mon_post_dinner", "mon_bedtime",

            # Tuesday
            "tue_pre_breakfast", "tue_post_breakfast", "tue_pre_lunch", "tue_post_lunch",
            "tue_pre_dinner", "tue_post_dinner", "tue_bedtime",

            # Wednesday
            "wed_pre_breakfast", "wed_post_breakfast", "wed_pre_lunch", "wed_post_lunch",
            "wed_pre_dinner", "wed_post_dinner", "wed_bedtime",

            # Thursday
            "thu_pre_breakfast", "thu_post_breakfast", "thu_pre_lunch", "thu_post_lunch",
            "thu_pre_dinner", "thu_post_dinner", "thu_bedtime",

            # Friday
            "fri_pre_breakfast", "fri_post_breakfast", "fri_pre_lunch", "fri_post_lunch",
            "fri_pre_dinner", "fri_post_dinner", "fri_bedtime",

            # Saturday
            "sat_pre_breakfast", "sat_post_breakfast", "sat_pre_lunch", "sat_post_lunch",
            "sat_pre_dinner", "sat_post_dinner", "sat_bedtime",

            # Sunday
            "sun_pre_breakfast", "sun_post_breakfast", "sun_pre_lunch", "sun_post_lunch",
            "sun_pre_dinner", "sun_post_dinner", "sun_bedtime",
        ]

        widgets = {
            field: forms.CheckboxInput(attrs={"class": "form-check-input"})
            for field in fields
        }
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
