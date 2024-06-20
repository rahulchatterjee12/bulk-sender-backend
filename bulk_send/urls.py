from django.urls import path
from .views import CreateScheduleView, ScheduleDetailView

urlpatterns = [
    path("create-schedule/", CreateScheduleView.as_view(), name="create-schedule"),
    path("schedule/<int:id>/", ScheduleDetailView.as_view(), name="schedule-detail"),
]
