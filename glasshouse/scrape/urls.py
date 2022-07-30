from django.urls import path
from scrape.views import generate_cities_districts, scrape, scrape_file, clean, houses_list

urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('scrape_file/', scrape_file, name="scrape_file"),
  path('generate_cities_districts/', generate_cities_districts, name="generate_cities_districts"),
  path('', houses_list, name="home"),
  path('clean/', clean, name="clean"), # "name=" to call from html
]
