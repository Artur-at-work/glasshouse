from django.contrib import admin
from .models import House, SoldHouses, PriceHistory

admin.site.register(House)
admin.site.register(PriceHistory)
# Register your models here.
