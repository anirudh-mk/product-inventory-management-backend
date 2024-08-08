from django.urls import path

from api import views

urlpatterns = [
    path('product/', views.ProductAPI.as_view()),
    path('stock/', views.StockAPI.as_view()),
    path('stock/<str:id>/', views.StockAPI.as_view()),

]