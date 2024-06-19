from django.db import models

class ScheduleTask(models.Model):
    account = models.CharField(max_length=15)
    manual_input = models.TextField(blank=True, null=True)
    message = models.TextField()
    csv_file = models.FileField(upload_to='csv_files/')
    additional_file = models.FileField(upload_to='additional_files/')
    schedule_from = models.IntegerField()
    schedule_to = models.IntegerField()
    days = models.JSONField()
    weeks = models.IntegerField()
    time = models.TimeField()
    status = models.CharField(max_length=10, default='pending')  # pending or completed
    phone_numbers = models.JSONField()
    schedule_date = models.DateField()
