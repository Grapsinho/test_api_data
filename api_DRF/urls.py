from django.contrib import admin
from django.urls import path, include
from .views import allProductApi, ProductDetailAPIView

urlpatterns = [
    path("products/all", allProductApi.as_view(), name="allProductApi"),
    path("products/<str:search>", ProductDetailAPIView.as_view(), name="ProductDetailAPIView"),
]
