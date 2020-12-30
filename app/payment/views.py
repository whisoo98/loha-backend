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
from iamporter import *
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
def create_payment(request):
    client = Iamporter(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                       imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))
    body = json.dumps(request.data)

    """카드정보 또는 빌링키로 결제를 요청합니다
            카드정보를 지정하여 일회성 키인 결제를 요청할 수 있으며, 빌링키(customer_uid)를 지정해 재결제를 요청할 수 있습니다.
            카드정보와 빌링키가 모두 지정되면 일회성 결제 수행 후 해당 카드정보를 바탕으로 빌링키를 저장합니다.
            Args:
                merchant_uid (str): 가맹점 거래 고유번호
                customer_uid (str): string 타입의 고객 고유번호
                name (str): 주문명
                amount (float): 결제금액
                vat (float): 결제금액 중 부가세 금액 (파라메터가 누락되면 10%로 자동 계산됨)
                card_number (str): 카드번호 (dddd-dddd-dddd-dddd)
                expiry (str): 카드 유효기간 (YYYY-MM)
                birth (str): 생년월일6자리 (법인카드의 경우 사업자등록번호10자리)
                pwd_2digit (str): 카드비밀번호 앞 2자리 (법인카드의 경우 생략가능)
                pg (str): API 방식 비인증 PG설정이 2개 이상인 경우, 결제가 진행되길 원하는 PG사를 지정하실 수 있습니다.
                buyer_info (dict): 구매자 정보 (name, tel, email, addr, postcode)
                card_quota (int): 카드할부개월수. 2 이상의 integer 할부개월수 적용 (결제금액 50,000원 이상 한정)
                custom_data (str): 거래정보와 함께 저장할 추가 정보
            Returns:
                dict
            """

    try:
        if('customer_uid' in body):
            response = client.create_payment(
                custom_uid=body['custom_uid'],
                merchant_uid=body['merchant_uid'],
                name=body['name'],
                amount=body['amount'],
                vat=body['vat'],
                pg=body['pg'],
                buyer_info=body['buyer_info'],
                card_quota=body['card_quota']
            )
        else:
            response = client.create_payment(
                merchant_uid=body['merchant_uid'],
                name=body['name'],
                amount=body['amount'],
                vat=body['vat'],
                pg=body['pg'],
                card_number=body['card_number'],
                expiry=body['expiry'],
                birth=body['birth'],
                pwd_2digit=body['pwd_2digit'],
                buyer_info=body['buyer_info'],
                card_quota=body['card_quota']
            )
        '''merchant_uid="yADDAPASDDSA",
                    name="주문명",
                    amount=10000,
                    card_number="6060-4565-9705-1802",
                    expiry="2023-01",
                    birth="980331",
                    pwd_2digit="12",
                    buyer_info={
                        'name': "ㄴ이름",
                        'tel': "01000000000",
                        'email': "someone@example.com",
                        'addr': "사는 곳 주소",
                        'postcode': "00000",
                    }'''

        return Response(response)

    except ImportError as e:
        return Response(e.response)

@api_view(['POST'])
def cancel_payment(request):
    client = Iamporter(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
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
    client = Iamporter(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                       imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

    body = json.dumps(request.data)

    """아임포트 고유번호 또는 가맹점지정 고유번호로 결제내역을 확인합니다
            Args:
                imp_uid (str): 아임포트 고유번호
                merchant_uid (str): 결제요청 시 가맹점에서 요청한 merchant_uid. imp_uid와 merchant_uid 중 하나는 필수어야합니다. 두 값이 모두 넘어오면 imp_uid를 우선 적용합니다.
            Returns:
                dict
            """

    try:
        response = client.find_payment(
            imp_uid=body['imp_uid'],
            merchant_uid=body['merchant_uid'],
        )
        return Response(response)

    except Exception as e:
        return Response(e.code)




