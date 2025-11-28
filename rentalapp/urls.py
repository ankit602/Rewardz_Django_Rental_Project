from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.start_rental, name="start"),
    path("extend/<int:rental_id>/", views.extend_rental, name="extend"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("reports/", views.reports, name="reports"),

]
