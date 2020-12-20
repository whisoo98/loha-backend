from django.shortcuts import render
from django.http.response import  HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

from rest_framework.decorators import api_view,parser_classes
from rest_framework.views import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.request import Request

from clayful import Clayful
from iamporter import *
import json



# Create your views here.
'''
find_payment
cancel_payment
create_billkey
find_billkey
delete_billkey
create_payment
'''

def create_payment(request):
    client = Iamporter(imp_key="8605712299401734",
                       imp_secret="VoICY5nRMtnvAENACdBM0UePAUtOZMiUb0x96V1TppoZ3bAFpbrq5FgGzJuzvNuGO1QUXROmgcmkoWZO")

    body = json.loads(request.data)
    try:
        response = client.create_payment(
            merchant_uid=body['merchant_uid'],
            name=body['name'],
            amount=body['amount'],
            card_number=body['card_number'],
            expiry=body['expiry'],
            birth=body['birth'],
            pwd_2digit=body['pwd_2digit'],
            buyer_info=body['buyer_info'],
        )
        return Response(response)

    except Exception as e:
        return Response(e.code)


def cancel_payment(request):
    client = Iamporter(imp_key="8605712299401734",
                       imp_secret="VoICY5nRMtnvAENACdBM0UePAUtOZMiUb0x96V1TppoZ3bAFpbrq5FgGzJuzvNuGO1QUXROmgcmkoWZO")

    #imp_uid = None, merchant_uid = None, amount = None, tax_free = None, reason = None

    body = json.loads(request.data)
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
        return Response(e.code)


def find_payment(request):
    client = Iamporter(imp_key="8605712299401734",
                       imp_secret="VoICY5nRMtnvAENACdBM0UePAUtOZMiUb0x96V1TppoZ3bAFpbrq5FgGzJuzvNuGO1QUXROmgcmkoWZO")

    body = json.loads(request.data)
    try:
        response = client.find_payment(
            imp_uid=body['imp_uid'],
            merchant_uid=body['merchant_uid'],
        )
        return Response(response)

    except Exception as e:
        return Response(e.code)




