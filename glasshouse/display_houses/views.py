from django.shortcuts import render
from scrape.models import House, SoldHouses, TaiwanCity

print("DEBUG: from display_houses app")
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
    return render(request, "index.html", context)

def sold_houses_list(request):
    houses = SoldHouses.objects.all()[::-1]
    context = {
        'object_list' : houses,
    }
    return render(request, "sold_houses.html", context)

