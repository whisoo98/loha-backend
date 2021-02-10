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
import datetime

@api_view(['GET'])
def order_list_api(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Order = Clayful.Order

        options = {
            'customer': request.headers['Custom-Token'],
            'query': {
                'fields':'_id,total.price,done,tags,cancellation,'
                         'items._id,items.bundleItems._id,items.total.price,items.product,items.variant,'
                         'fulfillments,refunds,createdAt,'
                         'shipments._id'
            },
        }
        result = Order.list_for_me(options)
        headers = result.headers
        data = result.data



        for order in data:
            del(order['currency'])
            order['total']['price']['original'] = order['total']['price']['original']['raw']
            order['total']['price']['sale'] = order['total']['price']['sale']['raw']
            order['total']['price']['withTax'] = order['total']['price']['withTax']['raw']
            order['total']['price']['withoutTax'] = order['total']['price']['withoutTax']['raw']

            for item in order['items']:
                item['total']['price']['original'] = item['total']['price']['original']['raw']
                item['total']['price']['sale'] = item['total']['price']['sale']['raw']
                item['total']['price']['withTax'] = item['total']['price']['withTax']['raw']
                item['total']['price']['withoutTax'] = item['total']['price']['withoutTax']['raw']

                item['variant']['price']['original'] = item['variant']['price']['original']['raw']
                item['variant']['price']['sale'] = item['variant']['price']['sale']['raw']
                if item['variant']['discount']['value'] is not None:
                    item['variant']['discount']['value'] = item['variant']['discount']['value']['raw']
                item['variant']['discount']['discounted'] = item['variant']['discount']['discounted']['raw']
                del(item['variant']['weight'])
                del(item['variant']['width'])
                del(item['variant']['height'])
                del(item['variant']['depth'])
            order['createdAt'] = order['createdAt']['raw']
            if order['cancellation'] is not None:
                order['cancellation']['cancelledAt']=order['cancellation']['cancelledAt']['raw']

            fulfillments = order['fulfillments']
            for fulfillment in fulfillments:
                for item in fulfillment['items']:
                    item['item']['variant']['price']['original'] = item['item']['variant']['price']['original']['raw']
                    item['item']['variant']['price']['sale'] = item['item']['variant']['price']['sale']['raw']
                    if item['item']['variant']['discount']['value'] is not None:
                        item['item']['variant']['discount']['value'] = item['item']['variant']['discount']['value']['raw']
                    item['item']['variant']['discount']['discounted'] = item['item']['variant']['discount']['discounted']['raw']
                    del (item['item']['variant']['weight'])
                    del (item['item']['variant']['width'])
                    del (item['item']['variant']['height'])
                    del (item['item']['variant']['depth'])
                    item['quantity']=item['quantity']['raw']
                fulfillment['createdAt']=fulfillment['createdAt']['raw']
                fulfillment['updatedAt']=fulfillment['updatedAt']['raw']
                if fulfillment['status'] == 'arrived' and order['done'] == False:
                    Due = datetime.datetime.strptime(fulfillment['udpdatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    now = datetime.datetime.now()
                    if now >= Due + datetime.timedelta(days=7):
                        Order.mark_as_done(order['_id'],{})

        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        print(e)
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sync_inventory_api(request, order_id):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Order = Clayful.Order
        options = {
        }

        result = Order.sync_inventory(order_id, options)
        headers = result.headers
        data = result.data

        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

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

@api_view(['POST'])
def cancel_for_me_api(request, order_id):
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

        result = Order.cancel_for_me(order_id, payload, options)
        headers = result.headers
        data = result.data

        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

class OrderAPI(APIView):#주문 가져오기 수정 삭제

    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    def get(self, request, order_id):
        try:
            Order = Clayful.Order
            options = {
                'customer': request.headers['Custom-Token'],
                'query': {
                },
            }
            result = Order.get_for_me(order_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            Order = Clayful.Order
            payload = json.dumps(request.data['payload'])
            options = {
                'customer': request.headers['Custom-Token'],
            }

            result = Order.update_for_me(order_id, payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        try:

            Order = Clayful.Order
            options = {

            }

            result = Order.delete(order_id, options)
            headers = result.headers
            data = result.data

            return Response("주문 삭제가 완료되었습니다.")

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)


class RefundAcceptAPI(APIView): #환불 승인여부

    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    def post(self, order_id, refund_id):
        try:
            Order = Clayful.Order
            options = {
            }

            result = Order.accept_refund(order_id, refund_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, order_id, refund_id):
        try:
            Order = Clayful.Order
            options = {
            }

            result = Order.unaccept_refund(order_id, refund_id, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

class OrderMarkReceiveAPI(APIView):
    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    def post(self, request, order_id):
        try:

            Order = Clayful.Order

            options = {
                'customer': request.headers['Custom-Token'],
            }

            result = Order.mark_as_received_for_me(order_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        try:

            Order = Clayful.Order

            options = {
                'customer': request.headers['Custom-Token'],
            }

            result = Order.mark_as_not_received_for_me(order_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

class FulfillAPI(APIView):
    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    def post(self, request, order_id):
        try:
            Order = Clayful.Order

            payload = json.dumps(request.data['payload'])

            options = {
            }

            result = Order.create_fulfillment(order_id, payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            Order = Clayful.Order

            payload = json.dumps(request.data['payload'])

            options = {
            }
            fulfillment_id = request.data['fulfillment_id']
            result = Order.update_fulfillment(order_id, fulfillment_id, payload, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        try:

            Order = Clayful.Order

            options = {
            }
            fulfillment_id = request.data['fulfillment_id']
            result = Order.delete_fulfillment(order_id, fulfillment_id, options)

            headers = result.headers
            data = result.data

            return Response("삭제가 완료되었습니다.")

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)
