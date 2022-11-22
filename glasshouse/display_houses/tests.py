import pytest

from display_houses.views import houses_list
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_view():
    pass


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  test_user = User.objects.get(username="john")
  assert test_user.username == 'john'
