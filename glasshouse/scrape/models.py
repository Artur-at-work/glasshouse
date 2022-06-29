from django.db import models

class House(models.Model):
    house_id = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    size_m2 = models.FloatField()
    price = models.FloatField()
    price_per_m2 = models.FloatField()
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    url = models.TextField()
    image = models.URLField(null=True, blank=True)
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
    house_id = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    size_m2 = models.FloatField()
    price = models.CharField(max_length=100)
    price_per_m2 = models.FloatField()
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    url = models.TextField()
    image = models.URLField(null=True, blank=True)
# Create your models here.
