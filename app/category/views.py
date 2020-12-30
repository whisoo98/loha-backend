from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse,Http404
from django.conf import settings

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
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
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




