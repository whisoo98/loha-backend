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
def cancel_payment(request):
    client = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                     imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

    """승인된 결제를 취소합니다.
            Args:
                imp_uid (str): 아임포트 고유 번호
                merchant_uid (str): 가맹점지정 고유 번호. imp_uid와 merchant_uid 중 하나는 필수이어야합니다. 두 값이 모두 넘어오면 imp_uid를 우선 적용합니다.
                amount (float): 취소 요청 금액. 누락 시 전액을 취소합니다.
                tax_free (float): 취소 요청 금액 중 면세 금액. 누락 시 0원으로 간주합니다.
                reason (str): 취소 사유
            Returns:
                dict
            """

    body = json.dumps(request.data)

    try:

        response = client.cancel_payment(
            imp_uid=body['imp_uid'],
            merchant_uid=body['merchant_uid'],
            amount=body['amount'],
            tax_free=body['tax_free'],
            reason=body['reason'],
        )

        return Response(response)

    except Exception as e:
        return Response(e.response)

@api_view(['GET'])
def find_payment(request):
    client = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                     imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

    body = json.dumps(request.data)

    try:
        response = client.find(merchant_uid = body['order_id'])
        return Response(response)

    except Exception as e:
        return Response(e.message)




