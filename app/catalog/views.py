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


class CatalogAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def post(self, request):
        try:
            Catalog = Clayful.Catalog
            payload = request.data['payload']
            options = {

            }

            result = Catalog.create(payload, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:

            return Response(e.code)

    def get(self, request):
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
            return Response(data,status=HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code + ' '+e.message,status=e.status)

        except Exception as e:
            print(e)
            return Response("알 수 없는 오류가 발생하였습니다.",status=HTTP_400_BAD_REQUEST)


class CatalogDetailAPI(APIView):

    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def get(self, request, catalog_id):
        try:
            Catalog = Clayful.Catalog
            options = {
                'query': {

                },
            }

            result = Catalog.get(catalog_id, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:

            return Response(e.code)

    def put(self, request, catalog_id):
        try:
            Catalog = Clayful.Catalog
            payload = json.dumps(request.data['payload'])
            options = {

            }

            result = Catalog.update(catalog_id, payload, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:

            return Response(e.code)

    def delete(self, request, catalog_id):
        try:
            Catalog = Clayful.Catalog
            options = {

            }
            result = Catalog.delete(catalog_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:

            return Response(data)