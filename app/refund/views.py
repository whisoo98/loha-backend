from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse,Http404
from django.conf import settings

from rest_framework.status import *
from rest_framework import mixins
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from clayful import Clayful, ClayfulException
import datetime

# Create your views here.

@api_view(['POST'])
def request_refund_for_me_api(request, order_id):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Order = Clayful.Order
        payload = json.dumps(request.data['payload'])

        options = {
            'customer': request.headers['Custom-Token'],
        }

        result = Order.request_refund_for_me(order_id, payload, options)

        headers = result.headers
        data = result.data

        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cancel_refund_for_me_api(request, order_id, refund_id):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Order = Clayful.Order
        payload = json.dumps(request.data['payload'])

        options = {
            'customer': request.headers['Custom-Token'],
        }
        result = Order.cancel_refund_for_me(order_id, refund_id, payload, options)

        headers = result.headers
        data = result.data
        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

class RefundAcceptAPI(APIView): #환불 승인여부

    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    def post(self, order_id, refund_id):
        try:
            Order = Clayful.Order
            options = {
            }

            result = Order.accept_refund(order_id, refund_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, order_id, refund_id):
        try:
            Order = Clayful.Order
            options = {
            }

            result = Order.unaccept_refund(order_id, refund_id, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

#TODO:환불처리
# 1. 아임포트에 토큰 요청
# 2. 클레이풀에 결제 정보 조회
# 3. 1,2를 기반으로 아임포트에 환불요청
# 4. 클레이풀에 환불 동기화 -> webhook/restock
# 5. 응답보내줌

def Refund(payload):
    iamport_url = 'https://api.iamport.kr'
    info = {
        'imp_key':getattr(settings, 'IAMPORT_REST_KEY', None),
        'imp_secret':getattr(settings, 'IAMPORT_SECRET_REST_KEY', None)
    }
    # 1. 아임포트에 토큰 요청
    res_iamport = requests.request(method='POST',url=iamport_url+'/users/getToken',**info)['response']['access_token']

    # 2. 클레이풀에 결제 정보 조회
    Order = Clayful.Order
    res_clayful = Order.get(payload['order_id'], {})

    # 3. 1,2를 기반으로 아임포트에 환불요청
    info = {
        'merchant_uid': payload['order_id'],
        'amount': payload.get('amount'),  # 0이면 전액 취소
        'tax_free': payload.get('tax_free'),  # 0이면 0원 처리
        'checksum': payload.get('checksum'),
        'reason': payload.get('reason'),
        'refund_holder': payload.get('refund_holder'),
        'refund_bank': payload.get('refund_bank'),
        'refund_account': payload.get('refund_account'),
    }
    res_iamport = requests.request(method='POST',url=iamport_url+'/payments/cancel',**info)
    return res_iamport
