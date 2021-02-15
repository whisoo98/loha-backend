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
from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('',order_list_api),
    path('refund/<str:order_id>/', request_refund_for_me_api),
    path('refund/cancel/<str:order_id>/<str:refund_id>/', cancel_refund_for_me_api),
    path('cancel/<str:order_id>/', cancel_for_me_api),
    path('<str:order_id>/', OrderAPI.as_view()),
    path('<str:order_id>/receivemark/',OrderMarkReceiveAPI.as_view()),
    path('refund/accept/<str:order_id>/<str:refund_id>/',RefundAcceptAPI.as_view()),
    path('fulfill/<str:order_id>/',FulfillAPI.as_view())
]
