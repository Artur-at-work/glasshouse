import requests
import re

from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from scrape.models import House, PropertyCountByType, PriceHistory
from django.http import HttpResponse
from django.utils import timezone

# visualization
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objects import Scatter

from django.db import connection
import pandas as pd

import plotly.express as px


# Returns True if property count has changed
def has_new_property(soup):
    property_types = PropertyCountByType.objects.all()
    property_types.__dict__

    for count in soup.find_all('span',  {'class': 'count'}):
        ptype = count.previous_sibling.strip()
        if ptype in property_types and property_types[ptype] != count.text.strip("()"):
            # new property count doesn't match old count in db
            new_count = {ptype:new_count.text.strip("()")}
            property_types.update(new_count)
            return True
    return False

# def save_price_changes():
#     #price_history = PriceHistory.objects.all()
#     id = 127661523
#     house = House.objects.get(house_id=127661523)
    
#     if not PriceHistory.objects.filter(house_id=house.house_id).exists():
#         # save new house listing
#         print("Adding new house")
#         p = PriceHistory(house_id=house.house_id, price=house.price, rec_date=timezone.now())
#         p.save()
#         return
    
#     # FAIL: returned several mathes - need to iterate
#     # BUT: it's possible to have duplicates, since price may repeat itself. 
#     # switch to archive_prices()
#     house_history = PriceHistory.objects.get(house_id = id)
#     if house_history.price != house.price:
#         print("Price has changed. Saving to price history")
#         p = PriceHistory(house_id=house.house_id, price=house.price, rec_date=timezone.now())
#         p.save()

def archive_prices():
    for house in House.objects.all():
        p = PriceHistory(house_id = house.house_id, price = house.price, rec_date = timezone.now())
        p.save()
        print("Saving price record for %s" % house.house_id)


def scrape(request):
    url_base = "https://www.century21global.com"
    path = "/for-sale-residential/Taiwan/Yilan-City/Luodong-Township?sort=priceAsc"
    #save_houses_html(url_base, path)

    r = requests.get(url_base + path)
    soup = BeautifulSoup(r.content, 'html.parser')
    # with open("page1.html", 'wb') as outfile:
    #     outfile.write(r.content)
    # Parse single house page for Prce, Size, etc.
    #with open("page1.html") as fp:
    #    soup = BeautifulSoup(fp, 'html.parser')
    archive_prices()
    
    if not has_new_property(soup):
        # no updates on page, do nothing
        print("No updates in search results")
        return redirect("../")

    for result in soup.find_all('div',  {'class': 'search-result'}):
        # print(result.prettify())
        house = House()
        house.house_id = result.find('button', {'class': 'property-card-save-btn'}).get('data-property-id')
        house.address = result.find('span', {'class': 'property-address'}).text

        size_txt = result.find('div', {'class': 'size'}).text # 765 sq. ft. - 71.11 m2
        house.size_m2 = re.search('ft. - (.*) m2', size_txt).group(1) # 71.11

        house.price = result.find('span', {'dir': 'ltr'}).text

        house.price_per_m2 = round(float(house.price.replace('$','').replace(',','')) / float(house.size_m2), 2)

        # re.search in several identical spans with different text
        for span in result.find_all('span', {'class': 'search-result-label'}):
            if span.find(text=re.compile("bedrooms")): # 3 bedrooms - 1 bath
                house.bedrooms = span.text[:1]
                house.bathrooms = re.search('bedrooms - (.*) bath', span.text).group(1)
                break
        
        # if not house.bedrooms:
        #     house.bedrooms = 0
        # if not house.bathrooms :
        #     house.bathrooms = 0

        url_path = result.find('a', {'class': 'search-result-photo'}).get('href')
        house.url = url_base + url_path
        #house.image = result.find('div', {'class': 'search-result-img'}).text # 765 sq. ft. - 71.11 m2
        house.save()
        #break
    return redirect("../")
    # Create your views here.

def houses_list(request):
    houses = House.objects.all()[::-1]
    context = {
        'object_list': houses,
    }
    return render(request, "scrape/home.html", context)

def clean(request):
    houses = House.objects.all()
    houses.delete()
    return redirect("../")

def price_history(request):
    # direct call to Django SQLite
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM scrape_PriceHistory")
        row = cursor.fetchall()
    
    result_table = pd.DataFrame(row) # TODO: preserve column names
    print(list(result_table.columns))

    fig = px.line(result_table, x=2, y=1, color=3)
    fig.update_layout(title_text = 'Price History by House',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Price')
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return render(request, "scrape/price_history.html", context={'plot_div': plotly_plot_obj})
