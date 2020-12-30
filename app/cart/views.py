from django.shortcuts import render,redirect
from django.conf import settings

from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView,Response
from rest_framework.status import *
from rest_framework.request import Request

from clayful import Clayful
import json

# Create your views here.

class CartAPI(APIView):

    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def post(self, request): # 고객이 본인 장바구니 확인
        try:
            Cart = Clayful.Cart
            payload = json.dumps(request.data['payload'])
            options = {
                'customer': request.headers.get('custom_token'),
                'query': {

                },
            }
            result = Cart.get_for_me(payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

class CartItemAPI(APIView):

    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    def post(self, request): # 자신의 장바구니에 물품 추가

        try:
            Cart = Clayful.Cart
            payload = json.dumps(request.data['payload'])
            options = {
                'customer': request.headers.get('custom_token'),
            }

            result = Cart.add_item_for_me(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

    def put(self, request, items_id): # 자신의 장바구니에서 물품 수정
        try:
            Cart = Clayful.Cart
            payload = json.dumps(request.data['payload'])
            options = {
                'customer': request.headers.get('custom_token'),
            }

            result = Cart.update_item_for_me(items_id, payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

    def delete(self, request): # 자신의 장바구니에서 선택 품목삭제
        try:
            Cart = Clayful.Cart
            options = {
                'customer': request.headers.get('custom_token'),
            }
            
            item_ids = json.dumps(request.data) # 선택된 품목을 dict형으로 받음
            for item_id in item_ids['item_ids'].value: # dict의 item_id에 대해서 삭제 실행
                Cart.delete_item_for_me(item_id,options) #삭제

            return redirect('/') # 자신의 장바구니 화면으로 redirect

        except Exception as e:
            return Response(e.code, status=e.status)

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
                'customer': request.headers.get('custom_token'),
                'query' : {

                }
            }
            result = Cart.checkout_for_me('order', payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code, status=e.status)

