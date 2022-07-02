from django.db import models
from django.utils.timezone import now

class House(models.Model): 
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(default=now, blank=True)
    house_id = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    size_m2 = models.FloatField()
    price = models.FloatField()
    price_per_m2 = models.FloatField()
    bedrooms = models.IntegerField(null=True, blank=True, default = 0)
    bathrooms = models.IntegerField(null=True, blank=True, default = 0)
    url = models.TextField()
    image = models.URLField(null=True, blank=True)
    #newly_listed = models.BooleanField(default = False)
    status = models.CharField(max_length=100, blank=True, default="unlisted")
    # TODO: add year built from house page

    def __str__(self):
        return self.house_id

class PropertyCountByType(models.Model):
    property_type = models.CharField(max_length=100)
    property_count = models.IntegerField(null=True, blank=True)

class PriceHistory(models.Model):
    #house_id = models.ForeignKey('House', on_delete=models.CASCADE)
    house_id = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    rec_date = models.DateField()

    def __str__(self):
        return self.house_id

class SoldHouses(models.Model):
    #sold_date = models.DateTimeField(auto_now_add=True)
    #pub_date = models.DateTimeField(null=True, blank=True, default=datetime.date.today)
    house_id = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    size_m2 = models.FloatField()
    price = models.FloatField()
    price_per_m2 = models.FloatField()
    bedrooms = models.IntegerField(null=True, blank=True, default = 0)
    bathrooms = models.IntegerField(null=True, blank=True, default = 0)
    url = models.TextField()
    image = models.URLField(null=True, blank=True)
    newly_listed = models.BooleanField(default = False)
    
# Create your models here.
