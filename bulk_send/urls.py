from django.urls import path
from .views import CreateScheduleView, ScheduleDetailView,ScheduleRunner

urlpatterns = [
    path("create-schedule/", CreateScheduleView.as_view(), name="create-schedule"),
    path("schedule/<int:id>/", ScheduleDetailView.as_view(), name="schedule-detail"),
    path("runner",ScheduleRunner.as_view(),name="message_send")
]
