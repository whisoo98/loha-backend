from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import mixins
import json
import requests
import requests

def list_all_categories():
    url = "https://mekind.cafe24api.com/api/v2/categories"

    headers = {
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "",
        'X-Cafe24-Client-Id': "ehSKOHqFTiAKp4coWMTCaH"
        }

    response = requests.request("GET", url, headers=headers)
    return JsonResponse(response.json())

