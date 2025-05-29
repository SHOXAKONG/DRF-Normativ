from celery import shared_task
import time
from django.utils import timezone


@shared_task
def sleep_task(duration):
    time.sleep(duration)
    return f"Task Completed after {duration} seconds"

@shared_task
def timezone_now():
    print(f"Time zone {timezone.now()}")