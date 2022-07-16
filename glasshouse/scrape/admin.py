from django.contrib import admin
from .models import House, SoldHouses, PriceHistory, TaiwanCity, TaiwanDistrict 

admin.site.register(House)
admin.site.register(SoldHouses)
admin.site.register(PriceHistory)
admin.site.register(TaiwanCity)
admin.site.register(TaiwanDistrict)

