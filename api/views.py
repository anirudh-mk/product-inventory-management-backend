from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Products, Variant
from api.serializer import ProductSerializer, StockCreateSerializer, UserRegisterSerializer
from rest_framework.pagination import PageNumberPagination

from utils.permissions import JWTToken, CustamizePermission


# Create your views here.
class ProductAPI(APIView):
    authentication_classes = [CustamizePermission]

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
            pages = round(product_queryset.count()/10)
            paginator = PageNumberPagination()
            paginator.page_size = 10
            page = paginator.paginate_queryset(product_queryset, request)

            serializer = ProductSerializer(page, many=True)
            return Response({'response': serializer.data, 'pages': pages}, status=status.HTTP_200_OK)


class StockAPI(APIView):
    authentication_classes = [CustamizePermission]
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


class UserLoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None:
            return Response(
                data="please enter your username", status=status.HTTP_400_BAD_REQUEST)

        if password is None:
            return Response(data='please enter your password', status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token = JWTToken().generate(user)
            return Response(
                data=token,
                status=status.HTTP_200_OK
            )
        else:
            return Response(data='invalid username or password', status=status.HTTP_404_NOT_FOUND)
