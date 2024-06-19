import datetime
from django.utils import timezone
from .models import ScheduleTask

def check_pending_schedules():
    now = timezone.now()
    pending_schedules = ScheduleTask.objects.filter(status='pending', schedule_date__lte=now.date(), time__lte=now.time())
    
    for schedule in pending_schedules:
        # Perform the scheduled task (e.g., make calls)
        # Example placeholder for the task
        perform_task(schedule)

        # Update the status to 'completed'
        schedule.status = 'completed'
        schedule.save()

def perform_task(schedule):
    print(f"Executing task for schedule: {schedule.id}")
