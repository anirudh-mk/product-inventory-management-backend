from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Products, Variant
from api.serializer import ProductSerializer, StockCreateSerializer, UserRegisterSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.

class ProductAPI(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('product created successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            product_queryset = Products.objects.filter(id=id).first()
            serializer = ProductSerializer(product_queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            product_queryset = Products.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 10
            page = paginator.paginate_queryset(product_queryset, request)

            serializer = ProductSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class StockAPI(APIView):
    def post(self, request):
        product = request.data.get('product')
        serializer = StockCreateSerializer(data=request.data, context={'product': product})
        if serializer.is_valid():
            serializer.save()
            return Response('stock added successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        variant_instance = Variant.objects.filter(id=id).first()

        if not variant_instance:
            return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)

        variant_instance.delete()
        return Response({"success": "product deleted successfully"}, status=status.HTTP_200_OK)


class UserRegisterAPI(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data='user created successfully',status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)