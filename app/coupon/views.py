from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework import request, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser

from user.views import require_login

from clayful import Clayful, ClayfulException

import json
import requests

@api_view(['GET'])
def manager_coupon_list(request):
    try:
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

        Coupon = Clayful.Coupon

        options = {
            'query': {},
        }
        result = Coupon.list(options)
        count = Coupon.count(options).data
        headers = result.headers
        data = result.data
        data['Count'] = count

        return Response(data, status=status.HTTP_200_OK)

    except ClayfulException as e:

        return Response(e.code, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response("알 수 없는 예외가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)




class Coupon(APIView):

    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer
            options = {
                'customer': request.headers['Custom-Token'],
                'query': {},
            }
            customer_id = Customer.get_me(options).data['_id']
            payload = request.data['payload']

            options = {
            }
            result = Customer.add_coupon(customer_id, payload, options)
            data = result.data

            return Response(data, status=status.HTTP_200_OK)


        except ClayfulException as e:

            return Response(e.code, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response("알 수 없는 예외가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def get(self, request, result):
        try:

            Customer = Clayful.Customer
            options = {
                'customer': request.headers['Custom-Token'],
                'query': {

                },
            }
            count = Customer.count_coupons(options)
            result = Customer.list_coupons(options)

            headers = result.headers
            data = result.data
            data['Count'] = count.data

            return Response(data, status=status.HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def delete(self, request, result):
        try:
            coupon_ids = request.data['coupon_ids']

            Customer = Clayful.Customer
            options = {
                'customer': request.headers['Custom-Token'],
                'query': {

                },
            }
            
            for coupon_id in coupon_ids:
                Customer.delete_coupon_for_me(coupon_id, options)
                
            return Response("총 {}개 삭제되었습니다".format(len(coupon_ids)), status=status.HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=status.HTTP_400_BAD_REQUEST)