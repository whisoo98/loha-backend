from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import requests

from rest_framework import request
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse

# Create your views here.


def list_all_products(request):
    url = "https://mekind.cafe24api.com/api/v2/products"

    headers = {
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "",
        'X-Cafe24-Client-Id': "ehSKOHqFTiAKp4coWMTCaH"
    }
    response = requests.request("GET", url, headers=headers)
    return JsonResponse(response.json())


def get_a_product(request, product_no):
    url = "https://mekind.cafe24api.com/api/v2/products/"+str(product_no)

    headers = {
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "",
        'X-Cafe24-Client-Id': "ehSKOHqFTiAKp4coWMTCaH"
    }
    response = requests.request("GET", url, headers=headers)
    return JsonResponse(response.json())
