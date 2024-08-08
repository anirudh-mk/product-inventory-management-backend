from django.urls import path

from api import views

urlpatterns = [
    path('product/', views.ProductAPI.as_view()),
    path('product/<str:id>/', views.ProductAPI.as_view()),
    path('stock/', views.StockAPI.as_view()),
    path('stock/<str:id>/', views.StockAPI.as_view()),
    path('user/register/', views.UserRegisterAPI.as_view()),
    path('user/login/', views.UserLoginAPI.as_view()),
]