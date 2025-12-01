from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils import timezone
from ..models import GlucoseReading, Meal
from django.db.models import Avg, Min, Max, StdDev


def generate_pdf_report(user):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="glucosnap_report.pdf"'

    # Gather Data
    readings = GlucoseReading.objects.filter(user=user).order_by("timestamp")
    meals = Meal.objects.filter(user=user).order_by("timestamp")

    stats = readings.aggregate(
        avg=Avg("glucose_level"),
        min=Min("glucose_level"),
        max=Max("glucose_level"),
        std_dev=StdDev("glucose_level"),
    )

    context = {
        "user": user,
        "generated_at": timezone.now(),
        "readings": readings,
        "meals": meals,
        "stats": stats,
    }

    html_string = render_to_string("glucose_tracker/pdf_report.html", context)

    html = HTML(string=html_string)
    html.write_pdf(response)

    return response
