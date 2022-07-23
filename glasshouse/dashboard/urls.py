from django.urls import path
from dashboard.views import price_history

urlpatterns = [
  path('price_history/', price_history, name="price_history"),
]
