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

class MeasurementSchedule(models.Model):
    DAY_CHOICES = [
        ("mon", _("Monday")),
        ("tue", _("Tuesday")),
        ("wed", _("Wednesday")),
        ("thu", _("Thursday")),
        ("fri", _("Friday")),
        ("sat", _("Saturday")),
        ("sun", _("Sunday")),
    ]

    TIME_CHOICES = [
        ("pre_breakfast", _("Pre Breakfast")),
        ("post_breakfast", _("Post Breakfast")),
        ("pre_lunch", _("Pre Lunch")),
        ("post_lunch", _("Post Lunch")),
        ("pre_dinner", _("Pre Dinner")),
        ("post_dinner", _("Post Dinner")),
        ("bedtime", _("Bedtime")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="measurement_schedule")

    # Monday
    mon_pre_breakfast = models.BooleanField(_("Monday - Pre Breakfast"), default=False)
    mon_post_breakfast = models.BooleanField(_("Monday - Post Breakfast"), default=False)
    mon_pre_lunch = models.BooleanField(_("Monday - Pre Lunch"), default=False)
    mon_post_lunch = models.BooleanField(_("Monday - Post Lunch"), default=False)
    mon_pre_dinner = models.BooleanField(_("Monday - Pre Dinner"), default=False)
    mon_post_dinner = models.BooleanField(_("Monday - Post Dinner"), default=False)
    mon_bedtime = models.BooleanField(_("Monday - Bedtime"), default=False)

    # Tuesday
    tue_pre_breakfast = models.BooleanField(_("Tuesday - Pre Breakfast"), default=False)
    tue_post_breakfast = models.BooleanField(_("Tuesday - Post Breakfast"), default=False)
    tue_pre_lunch = models.BooleanField(_("Tuesday - Pre Lunch"), default=False)
    tue_post_lunch = models.BooleanField(_("Tuesday - Post Lunch"), default=False)
    tue_pre_dinner = models.BooleanField(_("Tuesday - Pre Dinner"), default=False)
    tue_post_dinner = models.BooleanField(_("Tuesday - Post Dinner"), default=False)
    tue_bedtime = models.BooleanField(_("Tuesday - Bedtime"), default=False)

    # Wednesday
    wed_pre_breakfast = models.BooleanField(_("Wednesday - Pre Breakfast"), default=False)
    wed_post_breakfast = models.BooleanField(_("Wednesday - Post Breakfast"), default=False)
    wed_pre_lunch = models.BooleanField(_("Wednesday - Pre Lunch"), default=False)
    wed_post_lunch = models.BooleanField(_("Wednesday - Post Lunch"), default=False)
    wed_pre_dinner = models.BooleanField(_("Wednesday - Pre Dinner"), default=False)
    wed_post_dinner = models.BooleanField(_("Wednesday - Post Dinner"), default=False)
    wed_bedtime = models.BooleanField(_("Wednesday - Bedtime"), default=False)

    # Thursday
    thu_pre_breakfast = models.BooleanField(_("Thursday - Pre Breakfast"), default=False)
    thu_post_breakfast = models.BooleanField(_("Thursday - Post Breakfast"), default=False)
    thu_pre_lunch = models.BooleanField(_("Thursday - Pre Lunch"), default=False)
    thu_post_lunch = models.BooleanField(_("Thursday - Post Lunch"), default=False)
    thu_pre_dinner = models.BooleanField(_("Thursday - Pre Dinner"), default=False)
    thu_post_dinner = models.BooleanField(_("Thursday - Post Dinner"), default=False)
    thu_bedtime = models.BooleanField(_("Thursday - Bedtime"), default=False)

    # Friday
    fri_pre_breakfast = models.BooleanField(_("Friday - Pre Breakfast"), default=False)
    fri_post_breakfast = models.BooleanField(_("Friday - Post Breakfast"), default=False)
    fri_pre_lunch = models.BooleanField(_("Friday - Pre Lunch"), default=False)
    fri_post_lunch = models.BooleanField(_("Friday - Post Lunch"), default=False)
    fri_pre_dinner = models.BooleanField(_("Friday - Pre Dinner"), default=False)
    fri_post_dinner = models.BooleanField(_("Friday - Post Dinner"), default=False)
    fri_bedtime = models.BooleanField(_("Friday - Bedtime"), default=False)

    # Saturday
    sat_pre_breakfast = models.BooleanField(_("Saturday - Pre Breakfast"), default=False)
    sat_post_breakfast = models.BooleanField(_("Saturday - Post Breakfast"), default=False)
    sat_pre_lunch = models.BooleanField(_("Saturday - Pre Lunch"), default=False)
    sat_post_lunch = models.BooleanField(_("Saturday - Post Lunch"), default=False)
    sat_pre_dinner = models.BooleanField(_("Saturday - Pre Dinner"), default=False)
    sat_post_dinner = models.BooleanField(_("Saturday - Post Dinner"), default=False)
    sat_bedtime = models.BooleanField(_("Saturday - Bedtime"), default=False)

    # Sunday
    sun_pre_breakfast = models.BooleanField(_("Sunday - Pre Breakfast"), default=False)
    sun_post_breakfast = models.BooleanField(_("Sunday - Post Breakfast"), default=False)
    sun_pre_lunch = models.BooleanField(_("Sunday - Pre Lunch"), default=False)
    sun_post_lunch = models.BooleanField(_("Sunday - Post Lunch"), default=False)
    sun_pre_dinner = models.BooleanField(_("Sunday - Pre Dinner"), default=False)
    sun_post_dinner = models.BooleanField(_("Sunday - Post Dinner"), default=False)
    sun_bedtime = models.BooleanField(_("Sunday - Bedtime"), default=False)

    def get_schedule_for_day(self, day):
        """Restituisce le misurazioni pianificate per un giorno specifico"""
        day_map = {
            "mon": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
            "tue": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
            "wed": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
            "thu": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
            "fri": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
            "sat": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
            "sun": ["pre_breakfast", "post_breakfast", "pre_lunch", "post_lunch", "pre_dinner", "post_dinner", "bedtime"],
        }

        if day not in day_map:
            return {}

        schedule = {}
        for time in day_map[day]:
            field_name = f"{day}_{time}"
            schedule[time] = getattr(self, field_name, False)

        return schedule

    def get_weekly_schedule(self):
        """Restituisce l'intero programma settimanale"""
        return {
            "mon": self.get_schedule_for_day("mon"),
            "tue": self.get_schedule_for_day("tue"),
            "wed": self.get_schedule_for_day("wed"),
            "thu": self.get_schedule_for_day("thu"),
            "fri": self.get_schedule_for_day("fri"),
            "sat": self.get_schedule_for_day("sat"),
            "sun": self.get_schedule_for_day("sun"),
        }

    def __str__(self):
        return f"{self.user.username}'s Measurement Schedule"
