import requests
import re
import os

from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from scrape.models import House, PropertyCountByType, SoldHouses
from display_houses.models import TaiwanCity, TaiwanDistrict
from django.utils import timezone

# Returns True if property count has changed
#def has_new_property(soup):
#    property_types = PropertyCountByType.objects.all()
#    property_types.__dict__

#    for count in soup.find_all('span',  {'class': 'count'}):
#        ptype = count.previous_sibling.strip()
#        if ptype in property_types and property_types[ptype] != count.text.strip("()"):
            # new property count doesn't match old count in db
#            new_count = {ptype:new_count.text.strip("()")}
#            property_types.update(new_count)
#            return True
#    return False

def get_page_soup(url):
    r = requests.get(url)
    dp("r_status_code", r.status_code)
    return BeautifulSoup(r.content, 'html.parser')


def save_to_db(soup, url_base):
    # TODO: "try" or return
    for result in soup.find_all('div',  {'class': 'search-result'}):
        address = ""
        country = ""
        district = ""
        city = ""
        size_m2 = 0
        price = 1
        price_per_m2 = 0
        bedrooms = 0
        bathrooms = 0
        status = "unlisted"

        house_id = result.find('button', {'class': 'property-card-save-btn'}).get('data-property-id')
        address = result.find('span', {'class': 'property-address'}).text

        size_str = result.find('div', {'class': 'size'}).text # "765 sq. ft. - 71.11 m2"
        size_m2 = float(re.search('ft. - (.*) m2', size_str).group(1).replace(",","")) # "71.11"

        price_str = result.find('span', {'dir': 'ltr'}).text
        price = float(price_str.replace('$','').replace(',',''))
        price_per_m2 = round(price / size_m2, 1)

        house_link = result.find('a', {'class': 'search-result-photo'}).get('href')
        house_url = url_base + house_link

        # re.search in several identical spans with different text
        for span in result.find_all('span', {'class': 'search-result-label'}):
            if span.find(text=re.compile("bedrooms")): # "3 bedrooms - 1 bath"
                bedrooms = span.text.split()[0]
                match = re.search('bedrooms - (.*) bath', span.text)
                if match is not None:
                    bathrooms = match.group(1)

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
        dp("update_or_create house_id", house_id)


def scrape(request):
    url_base = "https://www.century21global.com"
    #url_path = "/for-sale-residential/Taiwan/Keelung-City/Keelung-Township?pageNo=1"
    url_path = "/for-sale-residential/Taiwan?pageNo=1"
    soup = get_page_soup(url_base + url_path)
    total_results = soup.find('div',  {'class': 'total-search-results'}).text.replace(",","") # (7,465 Results)
    print("total_results:%s" %total_results)
    # 20 results per page. Adding 0.99 to "round" to last int page
    total_pages = int(re.findall(r'\b\d+\b', total_results)[0]) / 20 + 0.99
    print("total_pages:%s" %total_pages)
    # already on 1st page, start from 2nd
    for page in range(1, int(total_pages + 1)):
    #for page in range(1, 4):
        if page != 1: # Page 1 was loaded already
            url_path = url_path.split("pageNo=",1)[0] + "pageNo=" + str(page)
            soup = get_page_soup(url_base + url_path)
        dp("url_base+path", url_base + url_path)
        dp("page No.", page)
        save_to_db(soup, url_base)
    return redirect("../")


def houses_list(request):
    city_qs = TaiwanCity.objects.all()
    if request.method == 'POST':
        dp("request.method", request.method)
        city_filter =  request.POST.get('city-form')
        houses = House.objects.all().filter(city=city_filter)
    else:
        dp("request.method", request.method)
        houses = House.objects.all()
    context = {
        'object_list': houses,
        'city_qs' : city_qs,
    }
    return render(request, "scrape/home.html", context)


def clean(request):
    houses = House.objects.all()
    houses.delete()
    return redirect("../")


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


def generate_cities_districts(request):
    cities = House.objects.order_by().values('city').distinct()
    cities_districts = House.objects.order_by().values('city','district').distinct()

    for city in cities:
        c, created = TaiwanCity.objects.get_or_create(name=city['city'])
        for cd in cities_districts:
            if cd['city'] == city['city']:
                TaiwanDistrict.objects.update_or_create(name=cd['district'], city=c)
    return redirect("../")

#
# DEBUG functions
#
def dp(name, variable): 
    print("[debug] %s: %s" % (name, variable))

def get_file_soup(file_path):
    with open(file_path) as fp:
        return BeautifulSoup(fp, 'html.parser')

def scrape_file(request):
    url_base = "https://www.century21global.com"
    url_path = "/for-sale-residential/Taiwan/Yilan-City/Luodong-Township?pageNo=1"

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, "tests/page1.html")
    soup = get_file_soup(file_path)
    total_results = soup.find('div',  {'class': 'total-search-results'}).text

    # 20 results per page. Adding 0.99 to "round up" to last int page
    total_pages = int(re.findall(r'\b\d+\b', total_results)[0]) / 20 + 0.99
    dp("total_pages", total_pages)
    # Assume all houses sold unless found in search results
    House.objects.update(status="sold")
    
    for page in range(1, int(total_pages + 1)):
        if page != 1: # Page 1 was loaded already
            url_path = url_path[:-1] + str(page)
            file_path = file_path[:-6] + str(page) + ".html"
            soup = get_file_soup(file_path)

        print("file_path:%s" %file_path)
        save_to_db(soup, url_base)

    return redirect("../")

# def generate_districts(request):
#     cities_districts = House.objects.order_by().values('city','district').distinct()
#     #print(cities_districts)
#     for cd in cities_districts:
#         print("cd: %s" %cd)
#         c = TaiwanCity.objects.get(name=cd['city'])
#         print(c)
#         print(type(c))
#         TaiwanDistrict.objects.update_or_create(name=cd['district'], city=c)
#         #TaiwanDistrict.objects.get_or_create(name=cd['district'], city=c.id)
#     return redirect("../")

# def generate_cities(request):
#     cities = House.objects.order_by().values('city').distinct()
#     for city in cities:
#         TaiwanCity.objects.get_or_create(name=city['city'])
#     return redirect("../")

