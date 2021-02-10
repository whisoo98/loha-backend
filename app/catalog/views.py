from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse,Http404
from django.conf import settings

from rest_framework.status import *
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from clayful import Clayful,ClayfulException
import datetime

@api_view(['GET'])
def catalog_list(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Catalog = Clayful.Catalog

        options = {
            'query': {
                'limit' : 7
            },
        }

        result = Catalog.list(options)

        headers = result.headers
        data = result.data
        for catalog in data:
            catalog['createdAt']=catalog['createdAt']['raw']
            catalog['updatedAt']=catalog['updatedAt']['raw']
            '''
            if catalog['meta']['DeletedAt'] is not None:
                Due = catalog['meta']['DeletedAt']=catalog['meta']['DeletedAt']['raw']
                Due = datetime.datetime.strptime(Due, '%Y-%m-%dT%H:%M:%S.%fZ')
                if Due <= datetime.datetime.now():
                    Catalog.delete(catalog['_id'],{})
                    '''

        return Response(data,status=HTTP_200_OK)


    except ClayfulException as e:

        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:

        print(e)

        return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)