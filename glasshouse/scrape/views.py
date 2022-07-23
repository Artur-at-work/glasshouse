import requests
import re
import os
import datetime

from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from scrape.models import House, PropertyCountByType, SoldHouses, TaiwanCity
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect

from .plots import *

#from .forms import CityDropdown
from django.forms import ModelForm

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

def get_page_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')

def scrape(request):
    url_base = "https://www.century21global.com"
    url_path = "/for-sale-residential/Taiwan/Yilan-City/Luodong-Township?pageNo=1"
    soup = get_page_soup(url_base + url_path)
    total_results = soup.find('div',  {'class': 'total-search-results'}).text

    # 20 results per page. Adding 0.99 to "round" to last int page
    total_pages = int(re.findall(r'\b\d+\b', total_results)[0]) / 20 + 0.99

    # already on 1st page, start from 2nd
    #for page in range(2, int(total_pages + 1)):
    for page in range(1, 1):
        for result in soup.find_all('div',  {'class': 'search-result'}):
            # zero all vars before parsing?
            price = 1
            bedrooms = 0
            bathrooms = 0
            status = "unlisted"

            house_id = result.find('button', {'class': 'property-card-save-btn'}).get('data-property-id')
            address = result.find('span', {'class': 'property-address'}).text

            size_str = result.find('div', {'class': 'size'}).text # "765 sq. ft. - 71.11 m2"
            size_m2 = float(re.search('ft. - (.*) m2', size_str).group(1)) # "71.11"

            price_str = result.find('span', {'dir': 'ltr'}).text
            price = float(price_str.replace('$','').replace(',',''))
            price_per_m2 = round(price / size_m2, 1)

            house_link = result.find('a', {'class': 'search-result-photo'}).get('href')
            house_url = url_base + house_link

            if result.find('span', {'class': 'new-flag'}):
                status = "new"
            else:
                status = "listed"

            # re.search in several identical spans with different text
            for span in result.find_all('span', {'class': 'search-result-label'}):
                if span.find(text=re.compile("bedrooms")): # "3 bedrooms - 1 bath"
                    bedrooms = span.text[:1]
                    bathrooms = re.search('bedrooms - (.*) bath', span.text).group(1)
                elif span.find(text=re.compile("Taiwan")): #TODO: regex if other country
                    location = span.text.strip().split(',')
                    if len(location) != 3:
                        # missing location
                        continue

                    district = location[0].strip()
                    city = location[1].strip()
                    country = location[2].strip()

            if House.objects.filter(house_id = house_id).exists():
                House.objects.filter(house_id = house_id).update(status=status)
                if House.objects.filter(
                    house_id = house_id,
                    address = address,
                    district = district,
                    city = city,
                    country = country,
                    price = price,
                    size_m2 = size_m2,
                    bedrooms = bedrooms,
                    bathrooms = bathrooms,
                    url = house_url
                    ):
                    # already in db. Skip
                    continue

            # # Create/update the record
            house = House()
            house.house_id = house_id
            house.address = address
            house.district = district
            house.city = city
            house.country = country
            house.size_m2 = size_m2
            house.price = price
            house.price_per_m2 = price_per_m2
            house.url = house_url
            house.bedrooms = bedrooms
            house.bathrooms = bathrooms
            house.status = status
            house.date_modified = timezone.now()
            # TODO: save creation date to track the age of this listing. Don't edit when update()
            house.save()

            url_path = url_path[:-1] + str(page)
            soup = get_page_soup(url_base + url_path)
        #break


    return redirect("../")

def get_file_soup(file_path):
    with open(file_path) as fp:
        return BeautifulSoup(fp, 'html.parser')
 
# DEBUG: scrape from .html file
def scrape_file(request):
    url_base = "https://www.century21global.com"
    url_path = "/for-sale-residential/Taiwan/Yilan-City/Luodong-Township?pageNo=1"

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, "tests/page1.html")
    soup = get_file_soup(file_path)
    total_results = soup.find('div',  {'class': 'total-search-results'}).text

    # 20 results per page. Adding 0.99 to "round up" to last int page
    total_pages = int(re.findall(r'\b\d+\b', total_results)[0]) / 20 + 0.99

    # Assume all houses sold unless found in search results
    House.objects.update(status="sold")

    for page in range(1, int(total_pages + 1)):
        if page != 1: # Page 1 was loaded already
            url_path = url_path[:-1] + str(page)
            file_path = file_path[:-6] + str(page) + ".html"
            soup = get_file_soup(file_path)

        print("file_path:%s" %file_path)

        for result in soup.find_all('div',  {'class': 'search-result'}):
            # zero all vars before parsing?
            price = 1
            bedrooms = 0
            bathrooms = 0
            status = "unlisted"

            house_id = result.find('button', {'class': 'property-card-save-btn'}).get('data-property-id')
            address = result.find('span', {'class': 'property-address'}).text

            size_str = result.find('div', {'class': 'size'}).text # "765 sq. ft. - 71.11 m2"
            size_m2 = float(re.search('ft. - (.*) m2', size_str).group(1)) # "71.11"

            price_str = result.find('span', {'dir': 'ltr'}).text
            price = float(price_str.replace('$','').replace(',',''))
            price_per_m2 = round(price / size_m2, 1)

            house_link = result.find('a', {'class': 'search-result-photo'}).get('href')
            house_url = url_base + house_link

            # re.search in several identical spans with different text
            for span in result.find_all('span', {'class': 'search-result-label'}):
                if span.find(text=re.compile("bedrooms")): # "3 bedrooms - 1 bath"
                    bedrooms = span.text[:1]
                    bathrooms = re.search('bedrooms - (.*) bath', span.text).group(1)
                elif span.find(text=re.compile("Taiwan")): #TODO: regex if other country
                    location = span.text.strip().split(',')
                    if len(location) != 3:
                        # missing location
                        continue

                    district = location[0].strip()
                    city = location[1].strip()
                    country = location[2].strip()

            if result.find('span', {'class': 'new-flag'}):
                status = "new"
            else:
                status = "listed"

            # If no meaningful changes, then skip without updating
            if House.objects.filter(house_id = house_id).exists():
                print("Exists" + house_id)
                House.objects.filter(house_id = house_id).update(status=status) # doesn't affect modified_date
                if House.objects.filter(
                    house_id = house_id,
                    address = address,
                    district = district,
                    city = city,
                    country = country,
                    price = price,
                    size_m2 = size_m2,
                    bedrooms = bedrooms,
                    bathrooms = bathrooms,
                    url = house_url
                    ):
                    # already in db. Skip
                    print("Skipped" + house_id)
                    continue
            
            defaults = dict(
                address = address,
                district = district,
                city = city,
                country = country,
                size_m2 = size_m2,
                price = price,
                price_per_m2 = price_per_m2,
                url = house_url,
                bedrooms = bedrooms,
                bathrooms = bathrooms,
                status = status,
                date_modified = timezone.now()
            )
            House.objects.update_or_create(house_id=house_id, defaults=defaults)
    return redirect("../")


def city_list(request):
    pass

def houses_list(request):
    city_qs = TaiwanCity.objects.all()
    if request.method == 'POST':
        print("request.method: %s" %request.method)
        print("POST var: %s" % request.POST['city-form'])
        city_filter =  request.POST.get('city-form')
        houses = House.objects.all().filter(city=city_filter)
    else:
        print("request is not POST")
        houses = House.objects.all()
        #form = CityDropdown()
    #houses = House.objects.all()[::-1]
    print("city_qs:%s" %city_qs)
    context = {
        'object_list': houses,
        'city_qs' : city_qs,
    }
    return render(request, "scrape/home.html", context)

def clean(request):
    houses = House.objects.all()
    houses.delete()
    return redirect("../")

def price_history(request):
    plotly_plot_obj = plot_price_history()
    return render(request, "scrape/price_history.html", context={'plot_div': plotly_plot_obj})

def move_sold_houses():
    for h in House.objects.filter(status="sold"):
        SoldHouses.objects.create(
            date_published = h.date_published,
            house_id = h.house_id,
            address = h.address,
            district = h.district,
            city = h.city,
            country = h.country,
            size_m2 = h.size_m2,
            price = h.price,
            price_per_m2 = h.price_per_m2,
            bedrooms = h.bedrooms,
            bathrooms = h.bathrooms,
            url = h.url,
            image = h.image,
            status = h.status
        )
    House.objects.filter(status="sold").delete()