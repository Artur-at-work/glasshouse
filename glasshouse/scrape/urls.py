from django.urls import path
from scrape.views import price_history, scrape, scrape_file, clean, houses_list
#from display_houses.views import houses_list

urlpatterns = [
  path('scrape/', scrape, name="scrape"),
  path('scrape_file/', scrape_file, name="scrape_file"),
  path('', houses_list, name="home"), # TODO: overwrites the houses_list in display_houses app
  path('clean/', clean, name="clean"), # "name=" to call from html
  #path('price_history/', price_history, name="price_history"),
  #path('sold_houses/', sold_houses_list, name="sold_houses")
]
