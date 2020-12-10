"""loha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', Cart.as_view()),
    path('<str:customer_id>/', Cart.as_view()),
    path('items/',CartItem.as_view()),
    path('items/empty/', CartItem.as_view()),
    path('items/delete/<str:items_id>/', CartItem.as_view()),
    path('items/update/<str:items_id>/', CartItem.as_view()),
    path('checkout/',CartCheckout.as_view()),
]
