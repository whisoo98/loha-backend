from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from rest_framework import generics
from rest_framework import mixins

from .serializers import ListAllCategoriesSerializer

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ListCategorySerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)