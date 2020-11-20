from django.contrib import admin
from django.urls import path
from .views import check, get_code, get_access_code, get_access_code_with_refresh
from .models import Authentication

urlpatterns = [
    path('', check),
    path('token/', get_access_code),
    path('authorize/', get_code),
]
