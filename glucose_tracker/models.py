from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserProfile(models.Model):
    LANGUAGE_CHOICES = [
        ("it", _("Italian")),
        ("en", _("English")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    diagnosis_date = models.DateField(_("Diagnosis Date"), null=True, blank=True)
    target_glucose_min = models.IntegerField(
        _("Target Glucose Min (mg/dL)"), default=70
    )
    target_glucose_max = models.IntegerField(
        _("Target Glucose Max (mg/dL)"), default=180
    )
    language_preference = models.CharField(
        _("Language Preference"), max_length=2, choices=LANGUAGE_CHOICES, default="it"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class GlucoseReading(models.Model):
    MEASUREMENT_TYPE_CHOICES = [
        ("fasting", _("Fasting")),
        ("pre_breakfast", _("Pre Breakfast")),
        ("post_breakfast", _("Post Breakfast")),
        ("pre_lunch", _("Pre Lunch")),
        ("post_lunch", _("Post Lunch")),
        ("pre_dinner", _("Pre Dinner")),
        ("post_dinner", _("Post Dinner")),
        ("bedtime", _("Bedtime")),
        ("night", _("Night")),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="glucose_readings"
    )
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)
    glucose_level = models.IntegerField(_("Glucose Level (mg/dL)"))
    measurement_type = models.CharField(
        _("Measurement Type"), max_length=20, choices=MEASUREMENT_TYPE_CHOICES
    )
    notes = models.TextField(_("Notes"), blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = _("Glucose Reading")
        verbose_name_plural = _("Glucose Readings")

    def __str__(self):
        return f"{self.glucose_level} mg/dL - {self.get_measurement_type_display()} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"


class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ("breakfast", _("Breakfast")),
        ("lunch", _("Lunch")),
        ("dinner", _("Dinner")),
        ("snack", _("Snack")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)
    meal_type = models.CharField(
        _("Meal Type"), max_length=20, choices=MEAL_TYPE_CHOICES
    )
    description = models.TextField(
        _("Description"), blank=True, help_text=_("AI generated description")
    )
    photo = models.ImageField(_("Photo"), upload_to="meals/%Y/%m/%d/")
    estimated_calories = models.IntegerField(
        _("Estimated Calories"), null=True, blank=True
    )
    carbs_estimate = models.FloatField(_("Carbs Estimate (g)"), null=True, blank=True)
    manual_notes = models.TextField(_("Manual Notes"), blank=True)

    # Store raw AI response if needed for debugging or re-parsing
    ai_response_raw = models.JSONField(_("AI Response Raw"), null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
