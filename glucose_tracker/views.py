from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Min, Max
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
import json
from datetime import timedelta

from .models import GlucoseReading, Meal
from .forms import GlucoseReadingForm, MealForm
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
    if request.method == "POST":
        form = GlucoseReadingForm(request.POST)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.user = request.user
            reading.save()
            messages.success(request, _("Glucose reading added successfully."))
            return redirect("dashboard")
    else:
        form = GlucoseReadingForm(initial={"timestamp": timezone.now()})

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
                        meal.estimated_calories = analysis.get("calories")
                        meal.carbs_estimate = analysis.get("carbs")
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
