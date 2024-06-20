from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from bulk_send.cron import my_scheduled_task

class Command(BaseCommand):
    help = 'Set up periodic task to run every 2 minutes'

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )

        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='run scheduler',
            task=my_scheduled_task,
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Periodic task created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Periodic task already exists'))
