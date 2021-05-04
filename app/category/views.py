from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings

from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from clayful import Clayful


@api_view(['GET'])
@parser_classes((JSONParser,))
def collection_list(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    try:
        Collection = Clayful.Collection

        options = {
            'query': {
                'fields': 'name',
                'limit': 120,
                'page': request.GET.get('page', 1),
                'parent': 'none',  # 최상위 카테고리만 가져옴
            },
        }
        result = Collection.list(options)
        data = result.data

        for category in data:
            name = category['name']
            if name == '인플루엔서' or name == '별쇼 특별전':
                data.remove(category)

        return Response(data)

    except Exception as e:
        print(e)
        return Response("카테고리를 불러오지 못했습니다.")
