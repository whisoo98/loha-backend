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

def set_raw(order):
    order['currency']['rate'] = order['currency']['rate']['raw']
    order['total']['price']['original'] = order['total']['price']['original']['raw']
    order['total']['price']['sale'] = order['total']['price']['sale']['raw']
    order['total']['price']['withTax'] = order['total']['price']['withTax']['raw']
    order['total']['price']['withoutTax'] = order['total']['price']['withoutTax']['raw']

    order['total']['items']['price']['original'] = order['total']['items']['price']['original']['raw']
    order['total']['items']['price']['sale'] = order['total']['items']['price']['sale']['raw']
    order['total']['items']['price']['withTax'] = order['total']['items']['price']['withTax']['raw']
    order['total']['items']['price']['withoutTax'] = order['total']['items']['price']['withoutTax']['raw']
    order['total']['items']['discounted'] = order['total']['items']['discounted']['raw']
    order['total']['items']['taxed'] = order['total']['items']['taxed']['raw']

    order['total']['shipping']['fee']['sale'] = order['total']['shipping']['fee']['sale']['raw']
    order['total']['shipping']['fee']['original'] = order['total']['shipping']['fee']['original']['raw']
    order['total']['shipping']['fee']['withTax'] = order['total']['shipping']['fee']['withTax']['raw']
    order['total']['shipping']['fee']['withoutTax'] = order['total']['shipping']['fee']['withoutTax']['raw']
    order['total']['shipping']['discounted'] = order['total']['shipping']['discounted']['raw']
    order['total']['shipping']['taxed'] = order['total']['shipping']['taxed']['raw']

    order['total']['discounted']=order['total']['discounted']['raw']
    order['total']['taxed']=order['total']['taxed']['raw']
    order['total']['amount']=order['total']['amount']['raw']
    for tax in order['total']['taxes']:
        tax['taxed']=tax['taxed']['raw']
    order['total']['paid'] = order['total']['paid']['raw']
    order['total']['cancelled'] = order['total']['cancelled']['raw']
    order['total']['refunded'] = order['total']['refunded']['raw']
    if order['cancellation'] is not None:
        order['cancellation']['cancelledAt']=order['cancellation']['cancelledAt']['raw']

    for item in order['items']:
        item['total']['price']['original'] = item['total']['price']['original']['raw']
        item['total']['price']['sale'] = item['total']['price']['sale']['raw']
        item['total']['price']['withTax'] = item['total']['price']['withTax']['raw']
        item['total']['price']['withoutTax'] = item['total']['price']['withoutTax']['raw']
        item['total']['discounted'] = item['total']['discounted']['raw']
        item['total']['taxed'] = item['total']['taxed']['raw']
        item['price']['original'] = item['price']['original']['raw']
        item['price']['sale'] = item['price']['sale']['raw']
        item['price']['withTax'] = item['price']['withTax']['raw']
        item['price']['withoutTax'] = item['price']['withoutTax']['raw']
        item['variant']['price']['original']=item['variant']['price']['original']['raw']
        item['variant']['price']['sale']=item['variant']['price']['sale']['raw']
        item['variant']['discount']['discounted']=item['variant']['discount']['discounted']['raw']
        if item['variant']['discount']['value'] is not None:
            item['variant']['discount']['value']=item['variant']['discount']['value']['raw']
        item['variant']['weight']=item['variant']['weight']['raw']
        item['variant']['width']=item['variant']['width']['raw']
        item['variant']['height']=item['variant']['height']['raw']
        item['variant']['depth']=item['variant']['depth']['raw']
        item['quantity']=item['quantity']['raw']
        for discount in item['discounts']:
            if 'coupon' in discount:
                if discount['coupon']['discount']['min'] is not None:
                    discount['coupon']['discount']['min']=discount['coupon']['discount']['min']['raw']
                if discount['coupon']['discount']['max'] is not None:
                    discount['coupon']['discount']['max'] = discount['coupon']['discount']['max']['raw']
                if discount['coupon']['discount']['value'] is not None:
                    discount['coupon']['discount']['value']=discount['coupon']['discount']['max']['value']
            if discount['value'] is not None:
                discount['value']=discount['value']['raw']
            discount['discounted']=discount['discounted']['raw']
            discount['before']=discount['before']['raw']
            discount['after']=discount['after']['raw']
        item['discounted']=item['discounted']['raw']
        for tax in item['taxes']:
            tax['rate']=tax['rate']['raw']
            tax['taxed']=tax['taxed']['raw']
        item['taxed']=item['taxed']['raw']
        if 'unfulfilled' in item:
            item['unfulfilled']=item['unfulfilled']['raw']
    for shipment in order['shipments']:
        if shipment['rule']['free']['priceOver'] is not None:
            shipment['rule']['free']['priceOver']=shipment['rule']['free']['priceOver']['raw']
        shipment['rule']['criteria']['price']=shipment['rule']['criteria']['price']['raw']
        shipment['rule']['criteria']['weight']=shipment['rule']['criteria']['weight']['raw']
        shipment['rule']['weightOver']=shipment['rule']['weightOver']['raw']
        shipment['rule']['fee']=shipment['rule']['fee']['raw']
        shipment['fee']['original']=shipment['fee']['original']['raw']
        shipment['fee']['sale']=shipment['fee']['sale']['raw']
        shipment['fee']['withTax']=shipment['fee']['withTax']['raw']
        shipment['fee']['withoutTax']=shipment['fee']['withoutTax']['raw']
        for item in shipment['items']:
            item['variant']['price']['original']=item['variant']['price']['original']['raw']
            item['variant']['price']['sale']=item['variant']['price']['sale']['raw']
            if item['variant']['discount']['value'] is not None:
                item['variant']['discount']['value']=item['variant']['discount']['value']['raw']
            item['variant']['discount']['discounted']=item['variant']['discount']['discounted']['raw']
            item['variant']['weight']=item['variant']['weight']['raw']
            item['variant']['width']=item['variant']['width']['raw']
            item['variant']['height']=item['variant']['height']['raw']
            item['variant']['depth']=item['variant']['depth']['raw']
            item['quantity']=item['quantity']['raw']
            item['price']['original']=item['price']['original']['raw']
            item['price']['sale']=item['price']['sale']['raw']
            item['price']['withTax']=item['price']['withTax']['raw']
            item['price']['withoutTax']=item['price']['withoutTax']['raw']
        shipment['quantity']=shipment['quantity']['raw']
        shipment['discounted']=shipment['discounted']['raw']
        for tax in shipment['taxes']:
            tax['rate']=tax['rate']['raw']
            tax['taxed']=tax['taxed']['raw']
        shipment['taxed']=shipment['taxed']['raw']
    fulfillments = order['fulfillments']
    for fulfillment in fulfillments:
        for item in fulfillment['items']:
            item['item']['variant']['price']['original'] = item['item']['variant']['price']['original']['raw']
            item['item']['variant']['price']['sale'] = item['item']['variant']['price']['sale']['raw']
            if item['item']['variant']['discount']['value'] is not None:
                item['item']['variant']['discount']['value'] = item['item']['variant']['discount']['value']['raw']
            item['item']['variant']['discount']['discounted'] = item['item']['variant']['discount']['discounted']['raw']
            item['item']['variant']['weight']=item['item']['variant']['weight']['raw']
            item['item']['variant']['width']=item['item']['variant']['width']['raw']
            item['item']['variant']['height']=item['item']['variant']['height']['raw']
            item['item']['variant']['depth']=item['item']['variant']['depth']['raw']
            item['item']['quantity'] = item['item']['quantity']['raw']
            item['item']['price']['original']=item['item']['price']['original']['raw']
            item['item']['price']['sale']=item['item']['price']['sale']['raw']
            item['item']['price']['withTax']=item['item']['price']['withTax']['raw']
            item['item']['price']['withoutTax']=item['item']['price']['withoutTax']['raw']
            item['quantity'] = item['quantity']['raw']

        fulfillment['createdAt'] = fulfillment['createdAt']['raw']
        fulfillment['updatedAt'] = fulfillment['updatedAt']['raw']

    for transaction in order['transactions']:
        transaction['paid']=transaction['paid']['raw']
        transaction['cancelled']=transaction['cancelled']['raw']
        transaction['refunded']=transaction['refunded']['raw']
        transaction['createdAt']=transaction['createdAt']['raw']
        transaction['updatedAt']=transaction['updatedAt']['raw']

    order['createdAt']=order['createdAt']['raw']
    order['updatedAt']=order['updatedAt']['raw']
    if order['paidAt'] is not None:
        order['paidAt'] = order['paidAt']['raw']

    if order['receivedAt'] is not None:
        order['receivedAt'] = order['receivedAt']['raw']



    if 'refunds' in order:
        for refund in order['refunds']:
            refund['total']['price']['withTax']=refund['total']['price']['withTax']['raw']
            refund['total']['price']['withoutTax']=refund['total']['price']['withoutTax']['raw']
            refund['total']['items']['price']['withTax']=refund['total']['items']['price']['withTax']['raw']
            refund['total']['items']['price']['withoutTax']=refund['total']['items']['price']['withoutTax']['raw']
            refund['total']['items']['taxed']=refund['total']['items']['taxed']['raw']
            refund['total']['shipping']['fee']['withTax']=refund['total']['shipping']['fee']['withTax']['raw']
            refund['total']['shipping']['fee']['withoutTax']=refund['total']['shipping']['fee']['withoutTax']['raw']
            refund['total']['shipping']['taxed']=refund['total']['shipping']['taxed']['raw']
            refund['total']['taxed']=refund['total']['taxed']['raw']
            for tax in refund['total']['taxes']:
                tax['taxed']=tax['taxed']['raw']
            if refund['cancellation'] is not None:
                refund['cancellation']['cancelledAt']=refund['cancellation']['cancelledAt']['raw']
            for item in refund['items']:
                item['price']['withTax']=item['price']['withTax']['raw']
                item['price']['withoutTax']=item['price']['withoutTax']['raw']
                item['taxed']=item['taxed']['raw']
                for tax in item['taxes']:
                    tax['taxed']=tax['taxed']['raw']
                item['item']['variant']['price']['original']=item['item']['variant']['price']['original']['raw']
                item['item']['variant']['price']['sale']=item['item']['variant']['price']['sale']['raw']
                if item['item']['variant']['discount']['value'] is not None:
                    item['item']['variant']['discount']['value']=item['item']['variant']['discount']['value']['raw']
                item['item']['variant']['discount']['discounted']=item['item']['variant']['discount']['discounted']['raw']
                item['item']['variant']['weight']=item['item']['variant']['weight']['raw']
                item['item']['variant']['width']=item['item']['variant']['width']['raw']
                item['item']['variant']['height']=item['item']['variant']['height']['raw']
                item['item']['variant']['depth']=item['item']['variant']['depth']['raw']

                item['item']['quantity']=item['item']['quantity']['raw']
                item['item']['price']['original']=item['item']['price']['original']['raw']
                item['item']['price']['sale']=item['item']['price']['sale']['raw']
                item['item']['price']['withTax']=item['item']['price']['withTax']['raw']
                item['item']['price']['withoutTax']=item['item']['price']['withoutTax']['raw']
                item['quantity']=item['quantity']['raw']
            for shipment in refund['shipments']:
                shipment['fee']['withTax']=shipment['fee']['withTax']['raw']
                shipment['fee']['withoutTax']=shipment['fee']['withoutTax']['raw']
                shipment['taxed']=shipment['taxed']['raw']
                for tax in shipment['taxes']:
                    tax['taxed']=tax['taxed']['raw']
                for item in shipment['shipment']['items']:
                    item['variant']['price']['original'] = item['variant']['price']['original']['raw']
                    item['variant']['price']['sale'] = item['variant']['price']['sale']['raw']
                    if item['variant']['discount']['value'] is not None:
                        item['variant']['discount']['value'] = item['variant']['discount']['value']['raw']
                    item['variant']['discount']['discounted'] = item['variant']['discount']['discounted']['raw']
                    item['variant']['weight'] = item['variant']['weight']['raw']
                    item['variant']['width'] = item['variant']['width']['raw']
                    item['variant']['height'] = item['variant']['height']['raw']
                    item['variant']['depth'] = item['variant']['depth']['raw']
                    item['quantity'] = item['quantity']['raw']
                    item['price']['original'] = item['price']['original']['raw']
                    item['price']['sale'] = item['price']['sale']['raw']
                    item['price']['withTax'] = item['price']['withTax']['raw']
                    item['price']['withoutTax'] = item['price']['withoutTax']['raw']
                shipment['shipment']['quantity']=shipment['shipment']['quantity']['raw']
                shipment['shipment']['fee']['original'] = shipment['shipment']['fee']['original']['raw']
                shipment['shipment']['fee']['sale'] = shipment['shipment']['fee']['sale']['raw']
                shipment['shipment']['fee']['withTax'] = shipment['shipment']['fee']['withTax']['raw']
                shipment['shipment']['fee']['withoutTax'] = shipment['shipment']['fee']['withoutTax']['raw']

            refund['createdAt']=refund['createdAt']['raw']
            refund['updatedAt']=refund['updatedAt']['raw']

    return order


@api_view(['GET'])
def order_list_api(request): #본인의 주문 내역 list
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

            },
        }
        result = Order.list_for_me(options)
        headers = result.headers
        data = result.data
        for order in data:
            order = set_raw(order)

        for order in data:
            del(order['tax'])
            del(order['customer'])
            if 'vendors' in order['total']:
                del(order['total']['vendors'])
            del(order['currency'])
            for item in order['items']:
                del(item['variant']['weight'])
                del(item['variant']['width'])
                del(item['variant']['height'])
                del(item['variant']['depth'])

            fulfillments = order['fulfillments']
            for fulfillment in fulfillments:
                for item in fulfillment['items']:
                    del (item['item']['variant']['weight'])
                    del (item['item']['variant']['width'])
                    del (item['item']['variant']['height'])
                    del (item['item']['variant']['depth'])
                if fulfillment['status'] == 'arrived' and order['done'] == False:
                    Due = datetime.datetime.strptime(fulfillment['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
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
def cancel_for_me_api(request, order_id): #본인의 주문 하나 취소
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

class OrderAPI(APIView):#주문 가져오기 수정

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
            print("@")
            data = set_raw(data)
            print("!")
            return Response(data)

        except ClayfulException as e:
            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            print(e)
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



class OrderMarkReceiveAPI(APIView): #주문 수령 체크
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


class FulfillAPI(APIView): #배송 생성 수정 삭제
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
