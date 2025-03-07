from scrape.models import House
from house_api.serializers import HouseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class HouseApiView(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class HouseApiView(APIView):
    class CustomPagination(PageNumberPagination):
        page_size = 10  # Adjust the page size as needed

    def get(self, request, *args, **kwargs):
        houses = House.objects.all()
        paginator = self.CustomPagination()
        paginated_houses = paginator.paginate_queryset(houses, request)
        serializer = HouseSerializer(paginated_houses, many=True)
        return paginator.get_paginated_response(serializer.data)


     
