from django.shortcuts import render
from django.http import JsonResponse

from scrape.models import House, SoldHouses
from display_houses.models import TaiwanCity, TaiwanDistrict

def houses_list(request):
    #city_qs = TaiwanCity.objects.all()
    houses = House.objects.all() 
    if request.method == 'POST':
        print("request.method: %s" %request.method)
        city_filter =  request.POST['city-menu']
        district_filter = request.POST['district-menu']
        if city_filter != "":
            houses = houses.filter(city=city_filter)
            if district_filter != "Choose District": # TODO: avoid grabbing default text
                houses = houses.filter(district=district_filter)
    else:
        print("request.method: %s" %request.method)
        houses = House.objects.all()
    context = {
        'object_list': houses,
        #'city_qs' : city_qs,
    }
    return render(request, "display_houses/index.html", context)

def sold_houses_list(request):
    houses = SoldHouses.objects.all()[::-1]
    context = {
        'object_list' : houses,
    }
    return render(request, "display_houses/sold_houses.html", context)

def get_json_city_data(request):
    city_val = list(TaiwanCity.objects.values())
    return JsonResponse({'data':city_val})

def get_json_district_data(request, *args, **kwargs):
    selected_city = kwargs.get('city')
    district_val = list(TaiwanDistrict.objects.filter(city__name=selected_city).values())
    return JsonResponse({'data':district_val})


