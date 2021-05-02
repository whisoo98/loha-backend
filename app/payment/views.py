import time

from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework import status

from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import Response, APIView
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.status import *
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from clayful import Clayful, ClayfulException
from iamport import *
from iamport.client import *
import json, pprint, datetime
from user.views import require_login


@api_view(['GET', 'POST'])
def verify_payment(request):
    try:
        # 아임포트 redirection

        imp_uid = request.data['imp_uid']
        merchant_uid = request.data['merchant_uid']
        amount = request.data['amount']

        '''
        아임포트에서 결제 내역 가져옴 & DB에서 결제 요청 내역 가져옴
        -> 가격 일치 판정
        '''

        # 토큰 받음
        iamport = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                          imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

        # 아임포트 결제 내역
        response = iamport.find(merchant_uid=merchant_uid)
        amount_paid = response['amount']
        status = response['status']

        # DB
        Order = Clayful.Order
        options = {
            'query': {}
        }
        result = Order.get(merchant_uid, options).data
        print(pprint.pformat(result))
        amount_to_be_paid = result['total']['price']['original']['raw']

        sms_key = getattr(settings, 'COOLSMS_API_KEY', None)
        sms_secret = getattr(settings, 'COOLSMS_API_SECRET', None)

        if int(amount_paid) == int(amount):  # 결제 금액 일치
            if status == 'ready':  # 가상계좌 발급

                # 가상계좌 발급 안내 알람 발송 - 문자
                vbank_num = response['vbank_num']  # 계좌번호
                vbank_date = response['vbank_date']  # 계좌만료일시
                vbank_name = response['vbank_name']  # 은행이름
                vbank_code = response['vbank_code']  # 은행 고유 코드
                vbank_holder = response['vbank_holder']  # 계좌소유주명
                vbank_issued_at = response['vbank_issued_at']  # 계좌 발급일시

                # mobile = str()
                # for a in result['address']['billing']['mobile'].split('-'):
                #     mobile += a
                #
                # params = dict()
                # params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
                # params['to'] = result['address']['billing']['mobile']  # Recipients Number '01000000000,01000000001'
                # params['from'] = getattr(settings,'BYEOLSHOW_PHONE',None)  # Sender number
                # params['text'] = 'Byeolshow 가상계좌 발급안내'+\
                #                  '\n'+\
                #                  '가상계좌 은행: '+vbank_name+\
                #                  '가상계좌 계좌번호: '+vbank_num+\
                #                  '입금하실 금액: '+str(amount_to_be_paid)  # Message
                # cool = Message(sms_key, sms_secret)
                # response = cool.send(params)
                content = {
                    'status': 'vbankIssued',
                    'message': '가상계좌 발급 성공',
                }
            elif status == 'paid':
                content = {
                    'status': 'success',
                    'message': '결제 성공',
                }
        else:
            iamport.cancel(reason="결제금액이 일치하지 않습니다.", merchant_uid=merchant_uid)

            # Order = Clayful.Order
            # payload = {
            #     'by': 'store',
            #     'reason': "결제금액이 일치하지 않습니다."
            # }
            # Order.cancel(merchant_uid, payload)
            #
            content = {
                'status': 'fail',
                'message': '결제 금익 불일치'
            }
        return Response(content)

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
        content = {
            "Error Code": e.code,
            "Error Message": e.msg,
        }
        return Response(content)

    except ClayfulException as e:
        print(e)
        print(e.code)
        print(e.message)
        return Response(e.code + ' ' + e.message, status=e.status)
    except Exception as e:
        print(e)
        return Response("에러발생")


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def test(request):
    try:
        print("IN")
        # 아임포트 redirection
        iamport = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                          imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))
        print("TOKEN")
        imp_uid = (request.data)['imp_uid']
        merchant_uid = (request.data)['merchant_uid']
        # imp_uid=request.data.get('imp_uid')
        # merchant_uid=request.data.get('merchant_uid')
        '''
        아임포트에서 결제 내역 가져옴 & DB에서 결제 요청 내역 가져옴
        -> 가격 일치 판정
        '''
        print("CHK1")
        # 토큰 받음

        sms_key = getattr(settings, 'COOLSMS_API_KEY', None)
        sms_secret = getattr(settings, 'COOLSMS_API_SECRET', None)

        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = '01059364069'
        params['from'] = '01021277076'
        params['text'] = '문자메시지문자메시지'
        content = {
            'status': 'vbankIssued',
            'message': '가상계좌 발급 성공',
        }
        cool = Message(sms_key, sms_secret)
        response = cool.send(params)

        # 아임포트 결제 내역
        response = iamport.find(merchant_uid=merchant_uid)
        print("CHK2")
        amount_paid = response['amount']
        status = response['status']
        print("SUC")
        if status == 'ready':  # 가상계좌 발급

            # TODO 가상계좌 발급 안내 알람 발송 - 문자

            content = {
                'status': 'vbankIssued',
                'message': '가상계좌 발급 성공',
            }
        else:
            content = {
                'status': 'success',
                'message': '결제 성공',
            }
        print("OUT")
        return Response(content)

    except Exception as e:
        print(e)
        return Response("에러 발생 백에 문의하세요")


@api_view(['GET'])
def pay_info(request):
    try:
        iamport = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                          imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))
        pay = iamport.find_by_merchant_uid(request.GET['order_id'])
        print(pay)
        return Response(pay, status=status.HTTP_200_OK)
    except Iamport.HttpError as e:
        if str(e) == "(404, 'Not Found')":
            return Response({}, status=status.HTTP_200_OK)
        else:
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        contents = {
            "error": {
                "message": "잘못된 요청입니다.",
                "detail": str(e)
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
