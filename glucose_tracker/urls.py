from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add-glucose/", views.add_glucose, name="add_glucose"),
    path("add-meal/", views.add_meal, name="add_meal"),
    path("glucose-history/", views.glucose_list, name="glucose_list"),
    path("meal-history/", views.meal_list, name="meal_list"),
    path("export/", views.export_data, name="export_data"),
    path("report/", views.generate_report, name="generate_report"),
    path("set-language/", views.set_language, name="set_language"),
    path("measurement-schedule/", views.measurement_schedule, name="measurement_schedule"),
]
