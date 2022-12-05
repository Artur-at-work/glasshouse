from rest_framework import serializers
from scrape.models import House

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['house_id', 'address', 'district', 'city', 'size_m2', 'price']

