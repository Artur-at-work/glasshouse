from django.urls import path
from scrape.views import price_history, scrape, scrape_file, houses_list, clean

urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('scrape_file/', scrape_file, name="scrape_file"),
  path('', houses_list, name="home"),
  path('clean/', clean, name="clean"),
  path('price_history/', price_history, name="price_history")
]
