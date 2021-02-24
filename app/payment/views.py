from django.shortcuts import render,redirect
from django.http.response import  HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import Response, APIView
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.status import *

from clayful import Clayful
from iamport import *
from iamport.client import *
import json

'''
IMP_PG_INICIS_WEBSTD = "html5_inicis"  # INICIS 웹표준
IMP_PG_INICIS_ACTIVEX = "inicis"  # INICIS Active-X
IMP_PG_NHNKCP = "kcp"  # NHNKCP
IMP_PG_NHNKCP_SUBSCRIBE = "kcp_billing"  # NHN KCP 정기결제
IMP_PG_LGUPLUS = "uplus"  # LG U+
IMP_PG_NICEPAY = "nice"  # 나이스페이
IMP_PG_JTNET = "jtnet"  # JTNet
IMP_PG_KAKAOPAY = "kakao"  # 카카오페이
IMP_PG_DANAL_PHONE = "danal"  # 다날휴대폰소액결제
IMP_PG_DANAL_GENERAL = "danal_tpay"  # 다날일반결제
IMP_PG_MOBILIANS = "mobilians"  # 모빌리언휴대폰소액결제
IMP_PG_SYRUPPAY = "syrup"  # 시럽페이
IMP_PG_PAYCO = "payco"  # 페이코
IMP_PG_PAYPAL = "paypal"  # 페이팔
IMP_PG_EXIMBAY = "eximbay"  # 엑심베이
IMP_PG_NAVERPAY = "naverco"  # 네이버페이
'''

@api_view(['POST'])
def verify_payment(request):
    
    #토큰 발급
    client = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                     imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

    try:
        #프론트로 부터 결제 정보 받음
        imp_uid=request.data.get('imp_uid')
        merchant_uid=request.data.get('merchant_uid')
        amount_to_be_paid = request.data['amount']
        #결제정보 조회
        response = client.find(imp_uid=imp_uid,merchant_uid=merchant_uid)
        is_paid = client.is_paid(amount=amount_to_be_paid, imp_uid=imp_uid,merchant_uid=merchant_uid)
        if is_paid is True: # 납부 완료
            content = {
                'status':'success',
                'message':'결제가 완료되었습니다.'
            }
            return Response(content)
        # 가상계좌는 현재로서는 구현하지 않음
        # elif response['status'] == 'ready': # 가상계좌
        #     # TODO: 카톡으로 가상계좌정보 보내기
        #     # webhook을 통해서 클레이풀에 가상계좌 정보 입력됨
        #     content = {
        #         'status': 'vbank',
        #         'message': '가상계좌가 발급되었습니다.'
        #     }
        #     return Response(content)
        else: # 결제 오류
            content = {
                'status':'fail',
                'message':'결제금액과 주문금액이 일치하지 않습니다.'
            }
            return Response(content)

    except Exception as e:
        print(e)
        print(e.code)
        print(e.message)
        return Response("에러 발생 백에 문의하세요", status=e.status)


def cancel_payment(order_id, refund_id):
    # 토큰 발급
    client = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                     imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

    try:

        Order = Clayful.Order
        order = Order.get(order_id, {}).data

        refunds = order['refunds']
        for refund in refunds: # target what i want 'refund'
            if refund['_id'] == refund_id:
                break

        merchant_uid = order_id
        cancel_request_amount = refund['total']['price']['withTax']
        reason = refund['reason']

        try:
            response = client.cancel(reason, merchant_uid=merchant_uid, amount=cancel_request_amount)
            return Response(response)
        except Iamport.ResponseError as e:
            print(e.code)
            print(e.message)  # 에러난 이유를 알 수 있음
            return Response(e.code + ' ' + e.message, status=e.status)
        except Iamport.HttpError as http_error:
            print(http_error.code)
            print(http_error.reason)# HTTP not 200 에러난 이유를 알 수 있음
            return Response('알 수 없는 에러가 발생했습니다.')

    except Exception as e:
        return Response(e.response)
