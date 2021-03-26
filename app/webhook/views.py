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
from iamport.client import *
from clayful import Clayful, ClayfulException
# Create your views here.

@api_view(['POST'])
def Refund(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    iamport = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                      imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))
    try:
        order_id = request.data['params']['orderId']
        refund_id = request.data['params']['refundId']
        Order = Clayful.Order

        # 1. 환불 재고 동기화
        Order.restock_all_refund_items(order_id, refund_id, {})

        # 2. 환불 과정
        res_clayful = Order.get(order_id, {}).data
        refunds = res_clayful['refunds']
        for refund in refunds:
            if refund['_id'] == refund_id:
                break;

        # NOTICE: amount는 환불 규정에 따라서 다를 수 있음
        amount = refund['total']['price']['withTax']['raw']
        reason = refund['reason']

        # 3. 1,2를 기반으로 아임포트에 환불요청
        info = {
            'merchant_uid': order_id,
            'amount': amount,  # 0이면 전액 취소
            # 'tax_free': payload.get('tax_free'),  # 0이면 0원 처리
            # 'checksum': payload.get('checksum'),
            ## NOTICE: 가상계좌 환불 미구현
            # 'refund_holder': payload.get('refund_holder'),
            # 'refund_bank': payload.get('refund_bank'),
            # 'refund_account': payload.get('refund_account'),
        }
        res_imp = iamport.cancel(reason=reason, kwargs=info)
        # 환불처리문자
        return Response(res_imp)
    except ClayfulException as e:
        print(e.code)
        print(e.message)
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)
    except Iamport.ResponseError as e:
        print(e.code)
        print(e.message)
        return Response(e.code + ' ' + e.message)
    except Iamport.HttpError as http_error:
        print(http_error.code)
        print(http_error.reason)
        return Response("에러 발생")

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

