from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse,Http404

from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view
import json
import requests
from clayful import Clayful

@api_view(['GET'])
def collection_list(reqeust):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs'
    })
    try:
        Collection=Clayful.Collection

        options = {
            'query' : {
                'fields' : 'name',
                'sort' : 'createdAt',
            },
        }

        result = Collection.list(options)

        headers = result.headers
        data = result.data

        return HttpResponse(data)
        #return JsonResponse(result)


    except Exception as e:
        return HttpResponse('ERROR')


