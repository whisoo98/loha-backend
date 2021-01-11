from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser


from clayful import Clayful
import json
import requests

@api_view(['POST'],)
def add_coupon(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Customer = Clayful.Customer
        payload = request.data['payload']

        if payload is None:
            raise Exception("쿠폰이 없습니다.")

        options = {
        }

        customer_ids = request.data['customer_ids']

        ## 고객 본인이 쿠폰발급 어떻게?
        result = []
        for customer_id in customer_ids:
            res = {
                "customer_id" : customer_id
            }
            res.update((Customer.add_coupon(customer_id, payload, options)).data)

            result.append(res)

        return Response(result)


    except Exception as e:

        # Error case
        return Response(e.code)
