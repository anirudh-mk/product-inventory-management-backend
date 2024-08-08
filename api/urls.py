from django.urls import path

from api import views

urlpatterns = [
    path('product', views.ProductAPI.as_view())

]