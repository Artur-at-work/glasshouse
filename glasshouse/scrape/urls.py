from django.urls import path
from scrape.views import price_history, scrape, houses_list, clean

urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('', houses_list, name="home"),
  path('clean/', clean, name="clean"),
  path('price_history/', price_history, name="price_history")
  # path('', total_listings, name="total_listings"),
]
