from django.shortcuts import render


from rest_framework.decorators import api_view,parser_classes
from rest_framework.views import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from clayful import Clayful
import json
# Create your views here.

class Cart(APIView):
    Clayful.config({
                  'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjhhNzc5NzY4NTlhOTZlMzI3N2NlZmRmNmU2M2MyMmE5Yzk0MGY3NTA2OTk5MDAwMzU4Y2ZlY2MyYzc0NzJhMTIiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3NDkyMjc4LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJTNFdEVUxROVJLTEQifQ.k1TqaUQgs0hLb2DUygPHFApQKigTJnNIexUPq2Rdl4k',
                  # CART
                  'language': 'ko',
                  'currency': 'KRW',
                  'time_zone': 'Asia/Seoul',
                  'debug_language': 'ko',
                   }
    )
    def post(self, request):
        try:
            Cart = Clayful.Cart
            payload = json.loads(request.body)
            options = {
                'query': {

                },
            }
            result = Cart.get_for_me(payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

    def post(self, request, customer_id):
        try:
            Cart = Clayful.Cart
            payload = json.loads(request.body)
            options = {
                'query' : {

                },
            }
            result = Cart.get(customer_id, payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)


class CartItem(APIView):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjhhNzc5NzY4NTlhOTZlMzI3N2NlZmRmNmU2M2MyMmE5Yzk0MGY3NTA2OTk5MDAwMzU4Y2ZlY2MyYzc0NzJhMTIiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3NDkyMjc4LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJTNFdEVUxROVJLTEQifQ.k1TqaUQgs0hLb2DUygPHFApQKigTJnNIexUPq2Rdl4k',
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    def get(self, request):
        try:
            Cart = Clayful.Cart
            payload = json.loads(request.body)
            options = {
                'customer': request.session['token'],
            }

            result = Cart.add_item_for_me(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)

    def delete(self, request):
        try:
            Cart = Clayful.Cart
            options = {
                'customer': request.session['token'],
            }
            result = Cart.empty_for_me(options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

    def put(self, request, items_id):
        try:
            Cart = Clayful.Cart
            payload = json.loads(request.body)
            options = {
                'customer': request.session['token'],
            }
            result = Cart.update_item_for_me(items_id, payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

    def delete(self, request, items_id):
        try:
            Cart = Clayful.Cart
            options = {
                'customer': request.session['token'],
            }
            result = Cart.delete_item_for_me(items_id, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

class CartCheckout(APIView):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjhhNzc5NzY4NTlhOTZlMzI3N2NlZmRmNmU2M2MyMmE5Yzk0MGY3NTA2OTk5MDAwMzU4Y2ZlY2MyYzc0NzJhMTIiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3NDkyMjc4LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJTNFdEVUxROVJLTEQifQ.k1TqaUQgs0hLb2DUygPHFApQKigTJnNIexUPq2Rdl4k',
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    def post(self, request):
        try:
            Cart = Clayful.Cart
            payload = json.loads(request.body)
            options = {
                'customer': request.session['token'],
                'query' : {

                }
            }
            result = Cart.checkout_for_me('order', payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

