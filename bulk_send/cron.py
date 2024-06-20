from django.utils import timezone
from bulk_send.models import ScheduleTask


def my_scheduled_task():
    now = timezone.now()
    pending_schedules = ScheduleTask.objects.filter(
        status="pending", schedule_date__lte=now
    )

    for schedule in pending_schedules:
        for phone in schedule.phone_numbers:
            phone.status = "not send"
        schedule.status = "completed"
        schedule.save()

    print("Task Completed")
