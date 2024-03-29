from dashboard.views import price_history
from django.urls import path

from .views import (get_json_city_data, get_json_district_data, houses_list,
                    sold_houses_list)

urlpatterns = [
  path('', houses_list, name="index"),
  path('price_history/', price_history, name="price_history"),
  path('sold_houses/', sold_houses_list, name="sold_houses"),
  path('city-json/', get_json_city_data, name="city-json"),
  path('district-json/<str:city>/', get_json_district_data,
       name="district-json"),   # str:city is kwargs in views.py
]
