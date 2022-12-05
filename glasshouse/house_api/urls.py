from django.urls import path
from .views import HouseApiView

urlpatterns = [
    path('all/', HouseApiView.as_view()),
]