from django.utils import timezone
from bulk_send.models import ScheduleTask
from celery import shared_task
import requests

import logging

from core.celery import app


# Get an instance of the custom logger
logger = logging.getLogger('manual')

@shared_task
@app.task
def my_scheduled_task():
    logger.info("scheduler called")

    response = requests.get('http://127.0.0.1:8000/whatsapp/runner')
    if response.status_code== 200:
        logger.info("Massages has been send")

    logger.info("Task Completed")
