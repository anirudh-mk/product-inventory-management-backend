from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Products
from api.serializer import ProductSerializer


# Create your views here.

class ProductAPI(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('product created successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        product_queryset = Products.objects.all()
        serializer = ProductSerializer(product_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)