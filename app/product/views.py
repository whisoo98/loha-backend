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

# for vod
from media.models import *
from django.db.models import Q
from media.serializers import *


from clayful import Clayful,ClayfulException
import json
import pprint
import requests

# Create your views here.
def set_raw(dict):
    depth1 = {
        'price':['original','sale'],
        #'discount':['discounted'],
        'discount':['discounted','value'],
        'rating':['count','sum','average'],
        'variants':{
            'price':['original', 'sale'],
            #'discount':['discounted'],
            'discount':['discounted','value'],
            'weight':['weight'],
            'width':['width'],
            'height':['height'],
            'depth':['depth'],
            'quantity':['quantity']
        },
    }

    dict['totalReview']=dict['totalReview']['raw']
    dict['updatedAt']=dict['updatedAt']['raw']
    dict['createdAt']=dict['createdAt']['raw']

    for depth2 in depth1.keys():
        if depth2 != 'variants':
            for key in depth1[depth2]:
                if dict[depth2][key] is not None:
                    dict[depth2][key]=dict[depth2][key]['raw']
        else:
            for depth3 in depth1[depth2].keys():
                for items in dict['variants']:
                    for key in depth1[depth2][depth3]:
                        if (depth3 == 'price' or depth3 == 'discount'):
                            if items[depth3][key] is not None:
                                items[depth3][key]=items[depth3][key]['raw']
                        else:
                            if items[depth3] is not None:
                                items[depth3] = items[depth3]['raw']
    return dict


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
                    'available': True,
                    'collection': collection_id,
                    #'limit': 120,
                    'limit': 3,
                    'page': request.GET.get('page', 1),
                },
            }
            result = Product.list(options)
            headers = result.headers
            data = result.data
            for dict in data:
                dict = set_raw(dict)

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
                'query': {
                    #'fields' : '_id,name,summary,description,price,discount,shipping,available,brand,thumbnail,collections,options,variants,meta.stream_url'
                },
            }

            result = Product.get(product_id, options)
            headers = result.headers
            data = result.data

            # VOD 불러오기

            product_vod = MediaSerializer(
                MediaStream.objects.filter(vod_id__in = data['meta']['my_vod']).order_by('-started_at')
                , many=True)
            data['vod_list'] = product_vod.data

            data = set_raw(data)
            vendor = data['vendor']['_id']
            ShippingPolicy = Clayful.ShippingPolicy
            options['query']['vendor']=vendor
            shipping = ShippingPolicy.list(options).data
            data['shipping']['method'] =data['shipping']['methods'][0]
            del(data['shipping']['methods'])
            for ele in shipping:
                for rule in ele['rules']:
                    if rule['free']['priceOver'] is not None:
                        rule['free']['priceOver'] = rule['free']['priceOver']['raw']
                    rule['weightOver']=rule['weightOver']['raw']
                    rule['fee']=rule['fee']['raw']
                ele['createdAt']=ele['createdAt']['raw']
                ele['updatedAt']=ele['updatedAt']['raw']
            data['ShippingPolicy']=shipping[0]
            return Response(data)


        except ClayfulException as e:

            return Response(e.code + ' ' + e.message, status=e.status)
        except Exception as e:
            print(e)
            return Response('알 수 없는 오류가 발생했습니다.', status=HTTP_400_BAD_REQUEST)

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
                'q': request.data['search'],
                #'limit': 120,
                'limit':3,
                'page': request.POST.get('page', 1),
                'search': {
                    'name.ko' : '',
                },
                'searchMatch': 'partial',

            },
        }

        result = Product.list(options)

        headers = result.headers
        data = result.data
        for dict in data:
            dict = set_raw(dict)
        return Response(data)

    except Exception as e:
        return Response("잘못된 검색입니다.")

@api_view(['GET'])
def list_product_catalog(request, discount_type):
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
                'available': True,
                #'limit': 120,
                'limit': 3,
                'page': request.GET.get('page', 1),
                'discountType': discount_type,
                'discountValueMin':request.GET.get('min',0),

            },
        }
        if discount_type == 'percentage':
            options['query']['discountValueMax'] = request.GET.get('max',100)
        else:
            options['query']['discountValueMax'] = request.GET.get('max',None)
        result = Product.list(options)
        headers = result.headers
        data = result.data

        for dict in data:
            dict = set_raw(dict)

        return Response(data)

    except ClayfulException as e:
        return Response(e.code + " " + e.message, status=e.status)
    except Exception as e:
        return Response("알 수 없는 예외가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def about_this(request,collection_id='any'):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

     # 특정 콜렉션 ID 없으면 모두 부름
    try:
        Product = Clayful.Product
        options = {
            'query': {
                'available': True,
                'collection': collection_id,
                'limit': 10,
            },
        }
        result = Product.list(options)
        headers = result.headers
        data = result.data
        for dict in data:
            dict = set_raw(dict)

        return Response(data)

    except ClayfulException as e:
        return Response(e.code + " " + e.message, status=e.status)
    except Exception as e:
        return Response("알 수 없는 예외가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)