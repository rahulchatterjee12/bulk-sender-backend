from django.urls import path
from .views import CreateScheduleView

urlpatterns = [
    path('create-schedule/', CreateScheduleView.as_view(), name='create-schedule'),
]
