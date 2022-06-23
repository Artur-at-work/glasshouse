from django.urls import path
from scrape.views import scrape, houses_list, clean
urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('', houses_list, name="home"),
  path('clean/', clean, name="clean")
  # path('', total_listings, name="total_listings"),
]
