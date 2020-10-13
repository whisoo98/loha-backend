from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import mixins

from .models import Product
from .forms import RegisterForm
from .serializers import ProductSerializer

# Create your views here.

class ProductListAPI(generics.GenericAPIView,mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, * args, **kwargs):
        return self.list(request, *args, **kwargs)
        
class ProductDetailAPI(generics.GenericAPIView,mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, * args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

