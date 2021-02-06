from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse

from iamporter.errors import ImpUnAuthorized, ImpApiError
from iamporter import *
from pip._internal import req

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView, Response
from rest_framework.status import *
from rest_framework.request import Request

import requests
from payment.views import *
from clayful import Clayful, ClayfulException
from clayful.exception import ClayfulException
import json
import time
import pprint

# Create your views here.
def ship_raw(shipping):
    for shipment in shipping:
        for rule in shipment['rules']:
            for key in rule:
                if key == 'free':
                    if rule[key]['priceOver'] is not None:
                        rule[key]['priceOver'] = rule[key]['priceOver']['raw']
                else:
                    if rule[key] is not None:
                        rule[key] = rule[key]['raw']
        for region in shipment['regions']:
            for rule in region['rules']:
                for key in rule:
                    if key == 'free':
                        if rule[key]['priceOver'] is not None:
                            rule[key]['priceOver'] = rule[key]['priceOver']['raw']
                    else:
                        if rule[key] is not None:
                            rule[key] = rule[key]['raw']


    return shipping

def sort(data, shipping, product): #배송 조건등 필요
    shipping = ship_raw(shipping)
    print("W")
    convert = [{
        'vendor' : 'byeolshow',
        'items':[]
    }]
    for key in data['items']:
        dict_temp = {}
        if 'vendor' in key:
            chk = False
            for L in convert:
                if L['vendor'] == key['vendor']:
                    chk = True
                    dict_temp = L
                    break
            if chk:
                print("?")
                dict_temp['items'].append(key)
                print("!")
            else:
                convert.append({
                    'vendor':key['vendor'],
                    'items':[key],
                })
        else:
            for L in convert:
                if L['vendor'] == 'byeolshow':
                    dict_temp = L
                    break
            dict_temp['items'].append(key)

    for vendor in convert:
        for shipment in shipping:
            if vendor['vendor']==shipment['vendor']:
                vendor['ShippingPolicy']=shipment
    for item in convert:
        if not len(item['items']):
            convert.pop(convert.index(item))

    return convert

def set_raw(dict_):
    depth = {
        'items':{
            'addedAt':['addedAt'],
            'variant': {
                'price': {
                    'original':['original'],
                    'sale':['sale']
                },
                # 'discount':['discounted'],
                'discount': {
                    'discounted':['discounted'],
                    'value':['value']
                },
                'weight': ['weight'],
                'width': ['width'],
                'height': ['height'],
                'depth': ['depth'],
            },
            'quantity': ['quantity'],
            'discounted':['discounted'],
            'discounts':{
                'discounted':['discounted'],
                'value': ['value'],
                'before': ['before'],
                'after': ['after'],
            },
            'taxed':['taxed'],
            'price':{
                'original':['original'],
                'sale':['sale'],
                'withTax':['withTax'],
                'withoutTax':['withoutTax']
            },
            'total':{
                'price':{
                    'original':['original'],
                    'sale':['sale'],
                    'withTax':['withTax'],
                    'withoutTax':['withoutTax']
                },
                'discounted': ['discounted'],
                'taxed': ['taxed'],
            }
        },
        'currency':{
            'rate':['rate']
        },

        'total':{
            'price':{
                'original':['original'],
                'sale':['sale'],
                'withTax':['withTax'],
                'withoutTax':['withoutTax']
            },
            'discounted': ['discounted'],
            'taxed':['taxed'],
            'amount': ['amount'],
            'items':{
                'price': {
                    'original': ['original'],
                    'sale': ['sale'],
                    'withTax': ['withTax'],
                    'withoutTax': ['withoutTax']
                },
                'discounted': ['discounted'],
                'taxed': ['taxed'],
            },
            'shipping':{
                'fee':{
                    'original':['original'],
                    'sale':['sale'],
                    'withTax':['withTax'],
                    'withoutTax':['withoutTax']
                },
                'discounted': ['discounted'],
                'taxed': ['taxed'],
            }
        }
    }
    for depth1 in depth.keys():
        t_dict = depth[depth1]
        #print('depth1 ' + depth1)
        if(depth1=='items'):
            for ele in dict_['items']:
                if isinstance(t_dict, dict):
                    for depth2 in t_dict.keys():
                        t2_dict = t_dict[depth2]
                        if(depth2=='discounts'):
                            for ele2 in ele['discounts']:
                                for depth3 in t2_dict.keys():
                                    if ele2[depth3] is not None:
                                        ele2[depth3] = ele2[depth3]['raw']

                        else:
                            #print('depth2 ' + depth2)
                            if isinstance(t2_dict, dict):
                                for depth3 in t2_dict.keys():
                                    #print('depth3 ' + depth3)
                                    t3_dict = t2_dict[depth3]
                                    if isinstance(t3_dict, dict):
                                        for depth4 in t3_dict.keys():
                                            #print('depth4 ' + depth4)
                                            if ele[depth2][depth3][depth4] is not None:
                                                ele[depth2][depth3][depth4] = ele[depth2][depth3][depth4]['raw']

                                    else:
                                        for key in t3_dict:
                                            if 'raw' in ele[depth2][key]:
                                                ele[depth2][key] = ele[depth2][key]['raw']

                            else:
                                for key1 in t2_dict:
                                    #print('key1 ' + key1)
                                    if 'raw' in ele[key1]:
                                        ele[key1] = ele[key1]['raw']
                else:
                    for key2 in t_dict:
                        #print('key2 ' + key2)
                        if 'raw' in dict_[depth1][key2]:
                            dict_[depth1][key2] = dict_[depth1][key2]['raw']
        else:
            if isinstance(t_dict,dict):
                for depth2 in t_dict.keys():
                    t2_dict = t_dict[depth2]
                    if isinstance(t2_dict, dict):
                        for depth3 in t2_dict.keys():
                            t3_dict = t2_dict[depth3]
                            if 'raw' in dict_[depth1][depth2][depth3]:
                                dict_[depth1][depth2][depth3]=dict_[depth1][depth2][depth3]['raw']
                    else:
                        for key1 in t2_dict:
                            if 'raw' in dict_[depth1][key1]:
                                dict_[depth1][key1]=dict_[depth1][key1]['raw']
            else:
                for key2 in t_dict:
                    if 'raw' in dict_[depth1][key2]:
                        dict_[depth1][key2]=dict_[depth1][key2]['raw']

    return dict_


class CartAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def post(self, request):  # 고객이 본인 장바구니 확인
        try:
            Cart = Clayful.Cart
            # payload = json.dumps(request.data['payload'])
            payload={}
            if 'payload' in request.data == True:
                payload = json.dumps(request.data['payload'])

            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                },
            }
            result = Cart.get_for_me(payload, options)
            headers = result.headers
            data = result.data
            return Response(data)
            for L in data['cart']['items']:
                var_id = L['variant']['_id']
                prod_id = L['product']['_id']
                variants = Clayful.Product.get(prod_id,{
                    'query':{
                        'raw':True,
                        'fields':'variants._id,variants.quantity'
                    }
                }).data['variants']
                for quantity in variants:
                    if quantity['_id'] == var_id:
                        L['stock'] = quantity['quantity']

            data['cart'] = set_raw(data['cart'])

            ShippingPolicy = Clayful.ShippingPolicy
            shipping = ShippingPolicy.list({
                'query':{
                    'fields':'method,country,rules,regions,vendor',
                }
            }).data
            '''
            for l in shipping:
                if 'vendor' not in l:
                    l['vendor']='byeolshow'
            '''

            data['cart'] = sort(data['cart'],shipping)


            return Response(data, status=HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code, status=e.status)
        except Exception as e:
            print(e)
            return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, request):  # 고객이 본인 장바구니 비우기
        try:
            Cart = Clayful.Cart
            options = {
                'customer': request.headers.get('Custom-Token'),
            }
            result = Cart.empty_for_me(options)

            return Response("장바구니 비우기가 완료되었습니다.", status=HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code, status=e.status)
        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)


class CartItemAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def post(self, request):  # 자신의 장바구니에 물품 추가

        try:
            Cart = Clayful.Cart
            payload = (request.data['payload'])
            options = {
                'customer': request.headers['Custom-Token'],
            }
            cart = Cart.get_for_me({}, options).data
            cart_id = []
            for key in cart['cart']['items']:
                cart_id.append({
                    'variant_id':key['variant']['_id'],
                    'item_id': key['_id']
                })

            result = []
            for key in payload:
                isFind = 0
                for key2 in cart_id:
                    if (key['variant'] == key2['variant_id']):
                        isFind=1
                        result.append(Cart.update_item_for_me(key2['item_id'], key, options).data)
                        break
                if isFind == 0:
                    result.append(Cart.add_item_for_me(key, options).data)

            return Response(result, status=HTTP_200_OK)


        except ClayfulException as e:
            return Response(e.code, status=e.status)
        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)

    def put(self, request):  # 자신의 장바구니에서 물품 수정
        try:
            Cart = Clayful.Cart
            payloads = (request.data['payload'])
            options = {
                'customer': request.headers.get('Custom-Token'),
            }
            result = []
            for payload in payloads:
                result.append(Cart.update_item_for_me(payload['item_id'], payload['payload'], options).data)
            return Response(result, status=HTTP_200_OK)


        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, request):  # 자신의 장바구니에서 선택 품목삭제
        try:
            Cart = Clayful.Cart
            options = {
                'customer': request.headers.get('Custom-Token'),
            }

            item_ids = (request.data['item_ids'])  # 선택된 품목을 dict형으로 받음
            for item_id in item_ids:  # dict의 item_id에 대해서 삭제 실행
                Cart.delete_item_for_me(item_id, options)  # 삭제

            return Response("모두 삭제하였습니다.", status=HTTP_200_OK)


        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)


class CartCheckoutAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def post(self, request):
        try:
            Cart = Clayful.Cart
            payload = json.dumps(request.data['payload'])
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {

                }
            }
            result = Cart.checkout_for_me('order', payload, options)
            headers = result.headers
            data = result.data
            return Response(data, status=HTTP_200_OK)


        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)


'''

@api_view(['POST'])
def checkout_api(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        local_host = "http://127.0.0.1:8000/"
        #local_host = "https://byeolshowco.com/"
        Cart = Clayful.Cart
        #payload = json.dumps(request.data['payload'])
        payload ={
            'items': [
                {
                    '_id': 'XVRDYF6GMSBM',
                    'product': 'XVRDYF6GMSBM',
                    'variant': 'V2M5DQLM7J92',
                    'quantity': 1,
                    'shippingMethod': 'RYBX8LQ7R797',
                    'request': 'aa',

                    'addedAt': "2020-12-24"
                },
                {
                    '_id': '8DQGCQ6XRKA6',
                    'product': '8DQGCQ6XRKA6',
                    'variant': 'BXAKZUT45969',
                    'quantity': 1,
                    'shippingMethod': 'RYBX8LQ7R797',
                    'request': 'aa',

                    'addedAt': "2020-12-24"
                }
            ],
            'currency': 'KRW',
            'paymentMethod': 'clayful-iamport',


            'tags': [],
            'address': {
                'shipping': {
                    'name': {
                        'first': 'aa',
                        'last': 'aa',
                        'full': 'aa'
                    },
                    'company': 'aa',
                    'postcode': '12345',
                    'country': 'KR',
                    'state': 'aa',
                    'city': 'aa',
                    'address1': 'aa',
                    'address2': 'aa',
                    'mobile': "+82-10-1234-5678",
                },
                'billing': {
                    'name': {
                        'first': 'aa',
                        'last': 'aa',
                        'full': 'aa'
                    },
                    'company': 'aa',
                    'postcode': '12345',
                    'country': 'KR',
                    'state': 'aa',
                    'city': 'aa',
                    'address1': 'aa',
                    'address2': 'aa',
                    'mobile': "+82-10-1234-5678",
                }
            },
            'request': 'aa',
            'discount' : {
                'cart' : {
                    'coupon' : 'G2CE3SKV8ESP',
                },
            }

        }



        options = {
            'customer': request.headers.get('Custom-Token'),
            #'customer': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYxZThiZmVkMTFkNjUzMzcxYTg2ODU3ZGRhNzRmNzk0ZGNhZGM0MjZiNjViMjdmZThmMzQwY2U1NzZjYmRhMmQiLCJyb2xlIjoiY3VzdG9tZXIiLCJpYXQiOjE2MDk2NDEzNzYsImV4cCI6MTYxMDI0NjE3Niwic3ViIjoiQUI4WExBWVFONjY1In0.WUl39BqYWvs4b_6Y--W3YDRSr9ylqnY5wUydtKnH8Fs',

            'query' : {

            }
        }

        #result = Cart.checkout_for_me('order', payload, options) # 내 주문 내역에 기록

        null = None
        true = True
        false = False

        result = {
    "order": {
        "currency": {
            "base": {
                "code": "KRW",
                "precision": 0
            },
            "payment": {
                "code": "KRW",
                "precision": 0
            },
            "rate": 1
        },
        "tax": {
            "region": null,
            "included": true,
            "country": "KR"
        },
        "customer": {
            "name": {
                "first": null,
                "last": null,
                "full": "asdf"
            },
            "email": "asdf@asdf.com",
            "mobile": "111",
            "phone": null,
            "gender": null,
            "birthdate": null,
            "country": null,
            "language": null,
            "currency": null,
            "timezone": null,
            "_id": "AB8XLAYQN665",
            "connect": false,
            "groups": [],
            "userId": "asdf",
            "alias": null
        },
        "address": {
            "shipping": {
                "name": {
                    "first": "aa",
                    "last": "aa",
                    "full": "aa"
                },
                "company": "aa",
                "state": "aa",
                "address2": "aa",
                "mobile": "+82-10-1234-5678",
                "phone": null,
                "postcode": "12345",
                "country": "KR",
                "city": "aa",
                "address1": "aa"
            },
            "billing": {
                "name": {
                    "first": "aa",
                    "last": "aa",
                    "full": "aa"
                },
                "company": "aa",
                "state": "aa",
                "address2": "aa",
                "mobile": "+82-10-1234-5678",
                "phone": null,
                "postcode": "12345",
                "country": "KR",
                "city": "aa",
                "address1": "aa"
            }
        },
        "total": {
            "price": {
                "original": 62352905,
                "sale": 61119452,
                "withTax": 61119452,
                "withoutTax": 55563137
            },
            "items": {
                "price": {
                    "original": 12352905,
                    "sale": 11119452,
                    "withTax": 11119452,
                    "withoutTax": 10108592
                },
                "discounted": 1233453,
                "taxed": 1010860
            },
            "shipping": {
                "fee": {
                    "original": 50000000,
                    "sale": 50000000,
                    "withTax": 50000000,
                    "withoutTax": 45454545
                },
                "discounted": 0,
                "taxed": 4545455
            },
            "discounted": 1233453,
            "taxed": 5556315,
            "amount": 61119452,
            "taxes": [
                {
                    "key": "KR/VAT",
                    "taxed": 5556315
                }
            ],
            "vendors": [
                {
                    "price": {
                        "original": 50012312,
                        "sale": 50011083,
                        "withTax": 50011083,
                        "withoutTax": 45464620
                    },
                    "items": {
                        "price": {
                            "original": 12312,
                            "sale": 11083,
                            "withTax": 11083,
                            "withoutTax": 10075
                        },
                        "discounted": 1229,
                        "taxed": 1008
                    },
                    "shipping": {
                        "fee": {
                            "original": 50000000,
                            "sale": 50000000,
                            "withTax": 50000000,
                            "withoutTax": 45454545
                        },
                        "discounted": 0,
                        "taxed": 4545455
                    },
                    "taxes": [
                        {
                            "key": "KR/VAT",
                            "taxed": 4546463
                        }
                    ],
                    "vendor": "7YBYC2BSZ26N",
                    "discounted": 1229,
                    "taxed": 4546463,
                    "amount": 50011083
                }
            ]
        },
        "synced": true,
        "done": false,
        "tags": [],
        "reviews": [],
        "cancellation": null,
        "request": "aa",
        "paidAt": null,
        "receivedAt": null,
        "syncTriedAt": null,
        "_id": "BLNWAZDPUWDH",
        "items": [
            {
                "total": {
                    "price": {
                        "original": 12340593,
                        "sale": 11108369,
                        "withTax": 11108369,
                        "withoutTax": 10098517
                    },
                    "discounted": 1232224,
                    "taxed": 1009852
                },
                "price": {
                    "original": 12340593,
                    "sale": 11108369,
                    "withTax": 11108369,
                    "withoutTax": 10098517
                },
                "brand": null,
                "shippingMethod": "RYBX8LQ7R797",
                "request": "aa",
                "taxCategory": null,
                "bundleItems": [],
                "collections": [
                    {
                        "path": [
                            "D5B4H7G5E9E3"
                        ]
                    }
                ],
                "discounts": [
                    {
                        "overridden": null,
                        "coupon": "G2CE3SKV8ESP",
                        "type": "fixed",
                        "value": 1232224,
                        "discounted": 1232224,
                        "before": 12340593,
                        "after": 11108369
                    }
                ],
                "taxes": [
                    {
                        "name": "VAT",
                        "rate": 10,
                        "taxed": 1009852
                    }
                ],
                "_id": "6BWDKATP34HV",
                "product": "XVRDYF6GMSBM",
                "variant": "V2M5DQLM7J92",
                "quantity": 1,
                "type": "tangible",
                "discounted": 1232224,
                "taxed": 1009852,
                "unfulfilled": 1
            },
            {
                "total": {
                    "price": {
                        "original": 12312,
                        "sale": 11083,
                        "withTax": 11083,
                        "withoutTax": 10075
                    },
                    "discounted": 1229,
                    "taxed": 1008
                },
                "price": {
                    "original": 12312,
                    "sale": 11083,
                    "withTax": 11083,
                    "withoutTax": 10075
                },
                "brand": null,
                "shippingMethod": "RYBX8LQ7R797",
                "request": "aa",
                "taxCategory": null,
                "bundleItems": [],
                "collections": [],
                "discounts": [
                    {
                        "overridden": null,
                        "coupon": "G2CE3SKV8ESP",
                        "type": "fixed",
                        "value": 1229,
                        "discounted": 1229,
                        "before": 12312,
                        "after": 11083
                    }
                ],
                "taxes": [
                    {
                        "name": "VAT",
                        "rate": 10,
                        "taxed": 1008
                    }
                ],
                "_id": "MDURAX323WZ3",
                "product": "8DQGCQ6XRKA6",
                "variant": "BXAKZUT45969",
                "quantity": 1,
                "type": "tangible",
                "discounted": 1229,
                "taxed": 1008,
                "vendor": "7YBYC2BSZ26N",
                "unfulfilled": 1
            }
        ],
        "language": "ko",
        "status": "placed",
        "shipments": [
            {
                "rule": {
                    "free": {
                        "priceOver": 30000
                    },
                    "criteria": {
                        "price": 11108369,
                        "weight": 0
                    },
                    "weightOver": 0,
                    "fee": 3000
                },
                "fee": {
                    "original": 0,
                    "sale": 0,
                    "withTax": 0,
                    "withoutTax": 0
                },
                "items": [
                    "6BWDKATP34HV"
                ],
                "discounts": [],
                "taxes": [
                    {
                        "name": "VAT",
                        "rate": 10,
                        "taxed": 0
                    }
                ],
                "type": "bundled",
                "shippingPolicy": "J6734JDEUUJJ",
                "quantity": 1,
                "free": true,
                "discounted": 0,
                "taxed": 0,
                "_id": "TWT7V3C2C2ST"
            },
            {
                "rule": {
                    "free": {
                        "priceOver": null
                    },
                    "criteria": {
                        "price": 11083,
                        "weight": 0
                    },
                    "weightOver": 0,
                    "fee": 50000000
                },
                "fee": {
                    "original": 50000000,
                    "sale": 50000000,
                    "withTax": 50000000,
                    "withoutTax": 45454545
                },
                "items": [
                    "MDURAX323WZ3"
                ],
                "discounts": [],
                "taxes": [
                    {
                        "name": "VAT",
                        "rate": 10,
                        "taxed": 4545455
                    }
                ],
                "type": "bundled",
                "shippingPolicy": "K3S8GYHBG7KH",
                "quantity": 1,
                "free": false,
                "discounted": 0,
                "taxed": 4545455,
                "vendor": "7YBYC2BSZ26N",
                "_id": "PZRL4FY3J2CR"
            }
        ],
        "fulfillments": [],
        "refunds": [],
        "transactions": [
            {
                "paid": 0,
                "cancelled": 0,
                "refunded": 0,
                "vbanks": [],
                "createdAt": "2021-01-02T08:17:54.393Z",
                "updatedAt": "2021-01-02T08:17:54.393Z",
                "paymentMethod": "CABLZR2PSH5D"
            }
        ],
        "meta": {},
        "createdAt": "2021-01-02T08:17:54.389Z",
        "updatedAt": "2021-01-02T08:17:54.463Z"
    }
}
'''
'''
        customer = payload['order']['customer']
        addr = payload['order']['address']

        merchant_uid = customer['_id'] + datetime.datetime.now().strftime('%y.%m.%d')

        urls = local_host + 'product/' + str(payload['items'][0]['_id']) + '/'
        response = requests.get(url=urls).json()

        amount = result['order']['total']['amount']  # 주문금액
        card_number = request.data['card_number']  # 카드번호 (1234-1234-1234-1234)
        expiry = request.data['expiry']  # 카드만료일 (2022-12)
        birth = request.data['birth']  # 생연월일(981212) 법인카드인경우 10자리
        pwd_2digit = request.data['pwd_2digit']  # 카드비밀번호 앞 2자리 (법인카드 생략가능)
        pg = request.data['pg']  # pg사 지정

        buyer_info = {  # 주문명
            'name': customer['name'],  # 주문자 이름
            'tel': customer['mobile'],  # 주문자 연락처
            'email': customer['email'],  # 주문자 이메일
            'addr': addr['billing']['city']  # 주문자 주소
                    + addr['billing']['address1']
                    + addr['billing']['address1'],
            'postcode': addr['billing']['postcode'],  # 주문자 우편번호
        }

        card_quota = request.data.get('card_quota')  # 할부개월
        custom_data = payload['request']  # 요청사항'''
'''
        merchant_uid = result['order']['_id']
        amount = 1500
        card_number = '6060-4565-9705-1802'
        expiry = '2023-01'
        birth = '980331'
        pwd_2digit = '12'
        pg = 'html5_inicis'

        buyer_info = {  # 주문명
            'name': '김휘수',  # 주문자 이름
            'tel': '01021277076',  # 주문자 연락처
            'email': 'whisoo98@naver.com',  # 주문자 이메일
            'addr': '시흥시 대은로 104번길 25',
            'postcode': '12345'
        }

        card_quota = 0
        custom_data = '맛잇게 해주세요'
        name = '김휘수의 테스트 주문'

        order_info = dict(merchant_uid=merchant_uid,
                          name=name,
                          amount=amount,
                          card_number=card_number,
                          expiry=expiry,
                          birth=birth,
                          pwd_2digit=pwd_2digit,
                          pg=pg,
                          buyer_info=buyer_info,
                          card_quota=card_quota,
                          custom_data=custom_data,
                          )

        if (len(payload['items']) == 1):
            #name = response['name']
            pass

        elif (len(payload['items']) > 1):
            #name = response['name'] + ' 외 ' + str(len(payload['items'])-1) + '개' # 주문명
            pass



        pay_info = create_payment(merchant_uid=merchant_uid,
                                  name=name,
                                  amount=amount,
                                  card_number=card_number,
                                  expiry=expiry,
                                  birth=birth,
                                  pwd_2digit=pwd_2digit,
                                  pg=pg,
                                  buyer_info=buyer_info,
                                  card_quota=card_quota,
                                  custom_data=custom_data)

        #결제 검증 넘겨주기






        cancel_payment(merchant_uid=merchant_uid, amount=amount)




        return Response()

        #headers = result.headers
        #data = result.data
        #return Response(data)

    except ImpUnAuthorized as e: #아임포트 인증 실패
        # 주문삭제
        print(e)
        return Response(e.message)

    except ImpApiError as e:  # 아임포트 API 오류
        # 주문삭제
        print(e)
        return Response(e.response.message)

    except ClayfulException as e : #클레이풀 에러
        print(e)
        print(e.is_clayful)
        print(e.model)
        print(e.method)
        print(e.status)
        print(e.headers)
        print(e.code)
        print(e.message)
        return Response("클레이풀 에러입니다.")

    except KeyError as e: #결제 요소 부족
        # 주문삭제
        return Response(str(e.args[0]))

    except Exception as e:
        # 주문삭제
        print(e)
        print("EX")
        return Response(str(e.args[0]))
'''

