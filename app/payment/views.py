from django.shortcuts import render,redirect
from django.http.response import  HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework import request

from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import Response, APIView
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request
from rest_framework.status import *

from clayful import Clayful
from iamport import *
from iamport.client import *
import json, pprint, datetime
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

@api_view(['GET','POST'])
def verify_payment(request):
    
    try:
        #아임포트 redirection
        imp_uid=request.GET.get('imp_uid')
        merchant_uid=request.GET.get('merchant_uid')
        imp_success=request.GET.get('imp_success')

        if imp_success == True:
            '''
            아임포트에서 결제 내역 가져옴 & DB에서 결제 요청 내역 가져옴
            -> 가격 일치 판정
            '''

            #토큰 받음
            iamport = Iamport(imp_key=getattr(settings, 'IAMPORT_REST_KEY', None),
                             imp_secret=getattr(settings, 'IAMPORT_SECRET_REST_KEY', None))

            #아임포트 결제 내역
            response = iamport.find(merchant_uid=merchant_uid)
            amount_paid = response['amount']
            status = response['status']

            #DB
            Order = Clayful.Order
            options = {
                'query':{}
            }
            result = Order.get(merchant_uid, options).data
            amount_to_be_paid = result['total']['price']['original']['raw']

            if amount_paid == amount_to_be_paid: #결제 금액 일치
                if status=='ready': #가상계좌 발급

                    # TODO 가상계좌 발급 안내 알람 발송 - 카톡
                    content = {
                        'status':'vbankIssued',
                        'message':'가상계좌 발급 성공',
                    }
                else:
                    content = {
                        'status':'success',
                        'message':'결제 성공',
                    }
            else:
                content = {
                    'status': 'fail',
                    'message':'결제 금익 불일치'
                }
        else:
            error_code=request.GET.get('error_code')
            error_message=request.GET.get('error_message')
            content = {
                'status':'error',
                'message':error_message
            }
        return Response(content)

    except Exception as e:
        print(e)
        print(e.code)
        print(e.message)
        return Response("에러 발생 백에 문의하세요", status=e.status)

@api_view(['GET','POST'])
def redirect_page(request):
    imp_uid = request.GET.get('imp_uid',1)
    merchant_uid = request.GET.get('merchant_uid',2)
    imp_success = request.GET.get('imp_success',3)
    error_code = request.GET.get('error_code',4)
    error_message = request.GET.get('error_code',5)
    content = {
        'imp_uid':imp_uid,
        'merchant_uid':merchant_uid,
        'imp_success':imp_success,
        'error_code':error_code,
        'error_message':error_message
    }
    pprint.pprint(content)
    return render(request,'redirect_page.html',content)

@api_view(['GET'])
def demo(request):
    return render(request,'iamportdemo.html', {'merchant_uid' : datetime.datetime.now().strftime("%Y%m%d%H%M%S") })

@api_view(['GET','POST'])
@parser_classes([JSONParser])
def test(request):
    try:
        print("IN")
        #아임포트 redirection
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
        #토큰 받음


        #아임포트 결제 내역
        response = iamport.find(merchant_uid=merchant_uid)
        print("CHK2")
        amount_paid = response['amount']
        status = response['status']
        print("SUC")
        if status=='ready': #가상계좌 발급

            # TODO 가상계좌 발급 안내 알람 발송 - 카톡
            content = {
                'status':'vbankIssued',
                'message':'가상계좌 발급 성공',
            }
        else:
            content = {
                'status':'success',
                'message':'결제 성공',
            }
        print("OUT")
        return Response(content)

    except Exception as e:
        print(e)
        return Response("에러 발생 백에 문의하세요")
