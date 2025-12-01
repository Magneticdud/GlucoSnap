from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Min, Max
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
import json
from datetime import timedelta

from .models import GlucoseReading, Meal, MeasurementSchedule
from .forms import GlucoseReadingForm, MealForm, MeasurementScheduleForm
from .utils.ai_analyzer import analyze_meal_image


@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)

    # Recent Data
    recent_readings = GlucoseReading.objects.filter(user=user)[:5]
    recent_meals = Meal.objects.filter(user=user)[:5]

    # Statistics (Last 7 Days)
    readings_7d = GlucoseReading.objects.filter(
        user=user, timestamp__date__gte=last_7_days
    )
    avg_glucose = readings_7d.aggregate(Avg("glucose_level"))["glucose_level__avg"]

    # Chart Data Preparation
    dates = []
    values = []
    # Simple aggregation for chart (this could be optimized)
    chart_readings = readings_7d.order_by("timestamp")
    for reading in chart_readings:
        dates.append(reading.timestamp.strftime("%Y-%m-%d %H:%M"))
        values.append(reading.glucose_level)

    context = {
        "recent_readings": recent_readings,
        "recent_meals": recent_meals,
        "avg_glucose": round(avg_glucose, 1) if avg_glucose else 0,
        "chart_dates": json.dumps(dates),
        "chart_values": json.dumps(values),
    }
    return render(request, "glucose_tracker/dashboard.html", context)


@login_required
def add_glucose(request):
    # Pre-fill measurement type from URL parameter if provided
    initial_data = {"timestamp": timezone.now()}
    time_param = request.GET.get("time")
    if time_param and time_param in dict(GlucoseReading.MEASUREMENT_TYPE_CHOICES):
        initial_data["measurement_type"] = time_param

    if request.method == "POST":
        form = GlucoseReadingForm(request.POST)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.user = request.user
            reading.save()
            messages.success(request, _("Glucose reading added successfully."))
            return redirect("dashboard")
    else:
        form = GlucoseReadingForm(initial=initial_data)

    return render(request, "glucose_tracker/add_glucose.html", {"form": form})


@login_required
def add_meal(request):
    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user

            # AI Analysis if photo is present
            if meal.photo:
                try:
                    analysis = analyze_meal_image(meal.photo)
                    if "error" not in analysis:
                        meal.description = analysis.get("description", "")
                        # Validate and convert numeric fields safely
                        try:
                            meal.estimated_calories = int(analysis.get("calories", 0)) if analysis.get("calories") else None
                        except (ValueError, TypeError):
                            meal.estimated_calories = None
        
                        try:
                            meal.carbs_estimate = float(analysis.get("carbs", 0)) if analysis.get("carbs") else None
                        except (ValueError, TypeError):
                            meal.carbs_estimate = None
        
                        meal.ai_response_raw = analysis
                        messages.info(
                            request,
                            _("AI Analysis complete. Please review the details."),
                        )
                    else:
                        messages.warning(
                            request, f"AI Analysis failed: {analysis['error']}"
                        )
                except Exception as e:
                    messages.error(request, f"Error during AI analysis: {str(e)}")

            meal.save()
            messages.success(request, _("Meal added successfully."))
            return redirect("dashboard")
    else:
        form = MealForm(initial={"timestamp": timezone.now()})

    return render(request, "glucose_tracker/add_meal.html", {"form": form})


@login_required
def glucose_list(request):
    readings_list = GlucoseReading.objects.filter(user=request.user)
    paginator = Paginator(readings_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "glucose_tracker/glucose_list.html", {"page_obj": page_obj})


@login_required
def meal_list(request):
    meals_list = Meal.objects.filter(user=request.user)
    paginator = Paginator(meals_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "glucose_tracker/meal_list.html", {"page_obj": page_obj})


@login_required
def export_data(request):
    format_type = request.GET.get("format", "csv")
    from .utils.export_utils import export_to_csv, export_to_excel, export_to_ods

    if format_type == "xlsx":
        return export_to_excel(request.user)
    elif format_type == "ods":
        return export_to_ods(request.user)
    else:
        return export_to_csv(request.user)


@login_required
def generate_report(request):
    from .utils.pdf_generator import generate_pdf_report

    return generate_pdf_report(request.user)

from django.utils.translation import activate
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def set_language(request):
    language = request.GET.get('language')
    next_url = request.GET.get('next', 'dashboard')

    if language and language in dict(UserProfile.LANGUAGE_CHOICES):
        # Update user's language preference
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.language_preference = language
        user_profile.save()

        # Activate the language for this session
        activate(language)

        # Set language cookie
        response = redirect(next_url)
        response.set_cookie('django_language', language)

        messages.success(request, _("Language changed successfully."))
        return response

    return redirect(next_url)

@login_required
def measurement_schedule(request):
    schedule, created = MeasurementSchedule.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MeasurementScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, _("Measurement schedule updated successfully."))
            return redirect("dashboard")
    else:
        form = MeasurementScheduleForm(instance=schedule)

    return render(request, "glucose_tracker/measurement_schedule.html", {"form": form})
