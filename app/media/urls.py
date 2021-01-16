from django.urls import path, include
from .views import *

urlpatterns = [
    path('reserve/', reserve_live),
    path('callback/', mux_callback),
]

