from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
import json
from clayful import Clayful

import requests

# Create your views here.

class ProductCollectionAPI(APIView):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs',
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def get(self, request, collection_id='any'):
        try:
            Product = Clayful.Product
            options = {
                'query': {
                    'available': True,
                    'collection': collection_id,
                },
            }
            result = Product.list(options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)


class ProductAPI(APIView):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs',
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    def post(self, request):
        try:
            Product = Clayful.Product
            payload = json.loads(request.body)
            options = {}
            result = Product.create(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)

    def get(self, request, product_id):
        try:
            Product = Clayful.Product
            options = {
                'query': {
                    'fields' : '_id,name,summary,description,price,discount,shipping,available,brand,thumbnail,collections,options,variants,meta.stream_url'
                },
            }
            result = Product.get(product_id, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)

    def put(self, request, product_id):
        try:
            Product = Clayful.Product
            payload = json.loads(request.body)
            options = {}
            result = Product.update(product_id, payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)

    def delete(self, request, product_id):
        try:
            Product = Clayful.Product
            options = {

            }
            result = Product.delete(product_id, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)


@api_view(['GET'])
@parser_classes((JSONParser,))
def product_searchAPI(request):

    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs',
        'language': 'ko',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    try:
        Product = Clayful.Product
        options = {
            'query': {
                'q': request.data['search'],
                #'search': request.data['search'],
                'search': {
                    'name.ko' : '',
                },
                'searchMatch': 'partial',

            },
        }

        result = Product.list(options)

        headers = result.headers
        data = result.data

        return Response(data)

    except Exception as e:

        return Response("EX")