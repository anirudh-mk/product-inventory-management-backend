from django.urls import path

from api import views

urlpatterns = [
    path('product/create/', views.ProductAPI.as_view())

]