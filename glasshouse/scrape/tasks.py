from celery import shared_task
from scrape.models import House, PropertyCountByType, PriceHistory
from django.utils import timezone
from celery.contrib import rdb

@shared_task
def archive_prices():
   for house in House.objects.all():
       p = PriceHistory(house_id = house.house_id, price = house.price, rec_date = timezone.now())
       p.save()
       print("Saving price record for %s" % house.house_id)

@shared_task
def say_hello(a):
    #rdb.set_trace()
    return "Hello %s" %a
