from django.urls import path
from display_houses.views import houses_list, sold_houses_list
from dashboard.views import price_history

urlpatterns = [
  path('', houses_list, name="index"),
  path('price_history/', price_history, name="price_history"),
  path('sold_houses/', sold_houses_list, name="sold_houses")
]
