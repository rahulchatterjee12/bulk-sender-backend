from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import csv
import io
from .models import ScheduleTask
from .serializers import ScheduleTaskSerializer
import datetime
import ast
import logging

logger = logging.getLogger('manual')

class ScheduleDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        logger.info(f'schedule details fetch fo schedule_id: {id}')
        schedule = get_object_or_404(ScheduleTask, id=id)
        serializer = ScheduleTaskSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ScheduleRunner(APIView):
    def get(self,request):
            now = timezone.now()
            current_date = now.date()
            current_time = now.time()

            pending_schedules = ScheduleTask.objects.filter(
                status="pending", schedule_date=current_date
            )
            for schedule in pending_schedules:
                for phone in schedule.phone_numbers:
                    phone['status'] = "not send"
                schedule.status = "completed"
                schedule.save()

            return Response([], status=status.HTTP_200_OK)

class CreateScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        account = request.data.get("account")
        manual_input = request.data.get("manual_input")
        message = request.data.get("message")
        if not message:
            return Response(
                {"error": "Message field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        csv_file = request.FILES["csv_file"]
        additional_file = request.FILES.get("additional_file")
        schedule_from = int(request.data.get("schedule_from"))
        schedule_to = int(request.data.get("schedule_to"))
        days = request.data.get("days")
        weeks = int(request.data.get("weeks"))
        time = request.data.get("time")

        phone_numbers = []
        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        for row in reader:
            phone_numbers.append({"number": row[0], "status": "pending"})

        # Calculate schedule dates
        start_date = timezone.now().date()
        created_schedules = []
        day_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }
        for week in range(weeks):
            temp_days = ast.literal_eval(days)
            for day in temp_days:
                day_index = day_map[day.lower()]
                next_date = start_date + datetime.timedelta(
                    days=(day_index - start_date.weekday() + 7) % 7 + week * 7
                )

                schedule_datetime = datetime.datetime.combine(
                    next_date, datetime.datetime.strptime(time, "%H:%M").time()
                )

                # Create one schedule task per schedule date
                schedule_task = ScheduleTask.objects.create(
                    account=account,
                    manual_input=manual_input,
                    message=message,
                    csv_file=csv_file,
                    additional_file=additional_file,
                    schedule_from=schedule_from,
                    schedule_to=schedule_to,
                    days=days,
                    weeks=weeks,
                    time=time,
                    phone_numbers=phone_numbers,
                    schedule_date=next_date,
                )
                created_schedules.append(schedule_task)

        return Response(
            {
                "status": "schedules created",
                "schedules": ScheduleTaskSerializer(created_schedules, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        schedules = ScheduleTask.objects.all()
        serializer = ScheduleTaskSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
