from rest_framework import serializers
from .models import ScheduleTask

class ScheduleTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleTask
        fields = '__all__'
