import json

from clayful import Clayful, ClayfulException
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *


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

# class RefundAcceptAPI(APIView): #환불 승인여부
#
#     def __init__(self):
#         Clayful.config({
#             'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
#             'language': 'ko',
#             'currency': 'KRW',
#             'time_zone': 'Asia/Seoul',
#             'debug_language': 'ko',
#         })
#
#     def post(self, order_id, refund_id):
#         try:
#             Order = Clayful.Order
#             options = {
#             }
#
#             result = Order.accept_refund(order_id, refund_id, options)
#
#             headers = result.headers
#             data = result.data
#
#             return Response(data)
#
#         except ClayfulException as e:
#             return Response(e.code + ' ' + e.message, status=e.status)
#
#         except Exception as e:
#             return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)
#
#     def delete(self, order_id, refund_id):
#         try:
#             Order = Clayful.Order
#             options = {
#             }
#
#             result = Order.unaccept_refund(order_id, refund_id, options)
#             headers = result.headers
#             data = result.data
#
#             return Response(data)
#
#         except ClayfulException as e:
#             return Response(e.code + ' ' + e.message, status=e.status)
#
#         except Exception as e:
#             return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)
