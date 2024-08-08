from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Products
from api.serializer import ProductSerializer
from rest_framework.pagination import PageNumberPagination


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

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(product_queryset, request)

        serializer = ProductSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)