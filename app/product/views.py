from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from rest_framework.status import *
from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser

from clayful import Clayful,ClayfulException
import json
import requests

# Create your views here.

class ProductCollectionAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def get(self, request, collection_id='any'): # 특정 콜렉션 ID 없으면 모두 부름
        try:
            Product = Clayful.Product
            options = {
                'query': {
                    'raw':True,
                    'available': True,
                    'collection': collection_id,
                },
            }
            result = Product.list(options)
            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code +" " + e.message, status=e.status)
        except Exception as e:
            return Response("알 수 없는 예외가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

class ProductAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    def post(self, request): #product 생성
        try:
            Product = Clayful.Product
            payload = json.dumps(request.data['payload'])
            options = {}
            result = Product.create(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

    def get(self, request, product_id): #product list'

        try:

            Product = Clayful.Product
            options = {
                'raw':True,
                'query': {
                    #'fields' : '_id,name,summary,description,price,discount,shipping,available,brand,thumbnail,collections,options,variants,meta.stream_url'
                },
            }
            result = Product.get(product_id, options)
            count = Clayful.Review.count_published({
                'query':{
                    'product':product_id
                }
            }).data['count']['raw']
            headers = result.headers
            data = result.data
            data['review_count'] = count

            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

    def put(self, request, product_id): #product 수정
        try:
            Product = Clayful.Product
            payload = json.dumps(request.data['payload'])
            options = {}
            result = Product.update(product_id, payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

    def delete(self, request, product_id): #product 삭제
        try:
            Product = Clayful.Product
            options = {

            }
            result = Product.delete(product_id, options)
            headers = result.headers
            data = result.data
            return redirect('/')

        except Exception as e:
            return Response(e.code, status=e.status)


@api_view(['POST'])
@parser_classes((JSONParser,))
def product_searchAPI(request):

    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    try:
        Product = Clayful.Product
        options = {
            'query': {
                'raw':True,
                'q': request.data['search'],
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
        return Response("잘못된 검색입니다.")