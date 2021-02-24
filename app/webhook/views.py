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

from refund.views import Refund
from payment.views import cancel_payment
# Create your views here.


@api_view(['POST'])
def restock_all_refund_items(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        order_id = request.data['params']['orderId']
        refund_id = request.data['params']['refundId']
        Order = Clayful.Order

        response = cancel_payment(order_id=order_id, refund_id=refund_id)

        Order.restock_all_refund_items(order_id, refund_id, {})

        # TODO: 환불 승인 문자 해주기
        # 환불처리가 승인되었습니다.


    except ClayfulException as e:
        print(e.code)
        print(e.message)
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def order_mark_done(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        order_id = request.data['params']['orderId']
        Order = Clayful.Order
        options = {
        }

        result = Order.mark_as_done(order_id, options)
        headers = result.headers
        data = result.data

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

