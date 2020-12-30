from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse,Http404

from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from clayful import Clayful

def config():
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM1MTUxMGVhM2IyYjkxMzllNmEwYzBiZDU5ODM1ZDg5OTBlYjFiZTY2NmVkYTcwNzgyNTRlOTdjZDQxZTI3N2IiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA5Mjk5MzM5LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJVM0dDTDZSWlVDVzMifQ.f6RndYqpY-ErnkYHq8EeP6Nkpg7bpcy1GGYeguKMtM0',
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

@api_view(['GET'])
@parser_classes((JSONParser,))
def collection_list(reqeust):

    config()

    try:
        Collection = Clayful.Collection

        options = {
            'query': {
                'fields': 'name',
                'parent': 'none', # 최상위 카테고리만 가져옴
            },
        }
        result = Collection.list(options)
        data = result.data
        return Response(data)
    
    except Exception as e:
        return Response(e.code)




