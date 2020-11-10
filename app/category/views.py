from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import mixins
import json
import requests

class ListAllCategoriesAPI(generics.GenericAPIView, mixins.ListModelMixin):
    def get_from_cafe24(self, request):
        #{}는 직접 따로 설정해야함
        url = "https://{mallid}.cafe24api.com/api/v2/admin/categories"

        headers = {
            'Authorization': "Bearer {access_token}",
            'Content-Type': "application/json",
            'X-Cafe24-Api-Version': "{version}"
        }
        
        response = requests.request("GET", url, headers=headers)
        return JsonResponse(response,status=200)


