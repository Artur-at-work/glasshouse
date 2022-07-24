from django.db import models
from django.utils.timezone import now
#from django import forms

class House(models.Model): 
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(default=now, blank=True)
    house_id = models.CharField(max_length=100) # TODO: non-editable after debug tests
    address = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    size_m2 = models.FloatField(null=True, blank=True)
    price = models.FloatField()
    price_per_m2 = models.FloatField()
    bedrooms = models.IntegerField(null=True, blank=True, default = 0)
    bathrooms = models.IntegerField(null=True, blank=True, default = 0)
    url = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=True, default="unlisted")
    # TODO: add year built from house page

    def __str__(self):
        return self.house_id

class PropertyCountByType(models.Model):
    property_type = models.CharField(max_length=100)
    property_count = models.IntegerField(null=True, blank=True)

# class PriceHistory(models.Model):
#     #house_id = models.ForeignKey('House', on_delete=models.CASCADE)
#     house_id = models.CharField(max_length=100)
#     price = models.CharField(max_length=100)
#     rec_date = models.DateField()

#     def __str__(self):
#         return self.house_id

class SoldHouses(models.Model):
    date_published = models.DateTimeField(null=True, blank=True)
    house_id = models.CharField(max_length=100) # TODO: non-editable after debug tests
    address = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    size_m2 = models.FloatField(null=True, blank=True)
    price = models.FloatField()
    price_per_m2 = models.FloatField()
    bedrooms = models.IntegerField(null=True, blank=True, default = 0)
    bathrooms = models.IntegerField(null=True, blank=True, default = 0)
    url = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True)
    date_sold = models.DateTimeField(default=now, editable=False, null=True, blank=True) # same approach in House?
    # TODO: add year built from house page

CITY_CHOICES = [
    ('*','---City---'),
    ('Taipei City','Taipei City'),
    ('New Taipei City','New Taipei City'),
    ('Taoyuan City','Taoyuan City'),
    ('Taichung City', 'Taichung City'),
    ('Yilan County','Yilan County'),
    ('Tainan City', 'Tainan City'),
    ('Taitung City', 'Taitung City'),
    ]

DISTRICT_CHOICES = [
    ('*', '---District---'),
    ('Luodong Township', 'Luodong Township'),
    ('Jiaoxi Township', 'Jiaoxi Township'),
]

# class TaiwanCity(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     country = models.CharField(max_length=100, null=True, blank=True, default="Taiwan")
    
#     def __str__(self):
#         return str(self.name)

# class TaiwanDistrict(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     city = models.ForeignKey(TaiwanCity, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.city}-{self.name}"