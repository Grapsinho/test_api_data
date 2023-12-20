from django.shortcuts import render
from inventory.models import Product, ProductInventory
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

# ესეიგი ეს ყველაფერი გვჭირდება ეიპიაისთვის

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from .serializers import *

from rest_framework.pagination import PageNumberPagination

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class allProductApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # მოკლედ ეს ორი გვჭირდება აუცილებლად სერიალაიზერ კლასი და მონაცემები
    queryset = ProductInventory.objects.all().select_related("product").order_by('id')
    serializer_class = ProductInventorySerializer
    permission_classes = []
    pagination_class = StandardResultsSetPagination

    # ესენი უკვე რაღაც ფუნქციაებია რომელიც იგივე რაღაცეებს აკეთებს
    # @method_decorator(cache_page(60 * 15))
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # @method_decorator(cache_page(60 * 15))
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import FloatField
class ProductDetailAPIView(generics.ListAPIView):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        search_query = self.kwargs.get('search', '')
        
        queryset = ProductInventory.objects.annotate(
            search=SearchVector('product__name', 'product__description'),
            rank=SearchRank(SearchVector('product__name', 'product__description'), SearchQuery(search_query))
        ).filter(
            Q(search=search_query) | Q(search__icontains=search_query)
        ).annotate(
            search_rank=Cast('rank', FloatField())
        ).order_by('-search_rank')  # Ordering by search rank (higher rank first)

        return queryset