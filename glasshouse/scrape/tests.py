#from django.test import TestCase
import pytest
from scrape.models import House


@pytest.mark.django_db
def test_house_create():
    house = House.objects.create(
        house_id="0123456789",
        address="1F, No. 11, Test Street 1",
        district="Test District",
        city="Test City",
        country="Test Country",
        size_m2="222.22",
        price="3333.33",
        bedrooms="4",
        price_per_m2=222.22/3333.33
    )
    # assert the assigned values
    assert house.house_id == "0123456789"
    assert house.address == "1F, No. 11, Test Street 1"
    assert house.district == "Test District"
    assert house.city == "Test City"
    assert house.country == "Test Country"
    assert house.size_m2 == "222.22"
    assert house.price == "3333.33"
    assert house.bedrooms == "4"

    # assert the default values
    assert house.status == "unlisted"
    assert house.bathrooms == 0
