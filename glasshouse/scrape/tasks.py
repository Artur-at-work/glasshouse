from celery import shared_task
from scrape.models import House
from dashboard.models import PriceHistory

from django.utils import timezone


@shared_task
@shared_task
def archive_prices():
    price_history_records = []
    for house in House.objects.all():
        price_history_records.append(PriceHistory(
            house_id=house.house_id,
            price=house.price,
            rec_date=timezone.now()
        ))
    PriceHistory.objects.bulk_create(price_history_records)  # Bulk create


@shared_task
def say_hello():
    return "Hello World from Celery tasks.py"
