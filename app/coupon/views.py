import datetime

from clayful import Clayful, ClayfulException
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from user.views import require_login
from .models import Coupon


@api_view(['GET'])
def manager_coupon_list(request):
    try:
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

        CCoupon = Clayful.Coupon

        options = {
            'query': {
                'limit': 120,
                'page': request.GET.get('page', 1)
            },
        }
        result = CCoupon.list(options)
        options = {
            'query': {}
        }
        headers = result.headers
        data = result.data
        for coupon in data:
            if coupon['expiresAt'] is not None:
                coupon['expiresAt'] = coupon['expiresAt']['raw']
                if datetime.datetime.strptime(coupon['expiresAt'],
                                              '%Y-%m-%dT%H:%M:%S.%fZ') < datetime.datetime.utcnow():
                    data.remove(coupon)
                    continue
            for discount in coupon['discount'].keys():
                if coupon['discount'][discount] is not None and discount != 'type':
                    coupon['discount'][discount] = coupon['discount'][discount]['raw']
            for amount in coupon['amount'].keys():
                if coupon['amount'][amount] is not None:
                    coupon['amount'][amount] = coupon['amount'][amount]['raw']
            for price in coupon['price'].keys():
                if coupon['price'][price] is not None:
                    coupon['price'][price] = coupon['price'][price]['raw']

            coupon['createdAt'] = coupon['createdAt']['raw']
            coupon['updatedAt'] = coupon['updatedAt']['raw']
            coupon['Issued'] = False

        Customer = Clayful.Customer
        if request.headers.get('Custom-Token') is not None:
            result = Customer.get_me({'customer': request.headers['Custom-Token'], 'query': {}})
            print(Coupon.objects.all())
            coupon_list = list(Coupon.objects.filter(user_id=result.data['_id']).all())
            for coupon in data:
                target = coupon['_id']
                for coupon_ele in coupon_list:
                    if target == coupon_ele.coupon_id:
                        coupon['Issued'] = True

        return Response(data, status=status.HTTP_200_OK)

    except ClayfulException as e:
        print(e.code)
        print(e.message)
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        print(e)
        return Response("알 수 없는 예외가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)


class CouponViewSet(APIView):

    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer
            customer_id = result.data['_id']
            payload = (request.data['payload'])
            coupon_id = payload['coupon']
            options = {
            }
            result = Customer.add_coupon(customer_id, payload, options)  # 고객에게 쿠폰 발급
            Coupon.objects.create(user_id=customer_id, coupon_id=coupon_id)

            return Response(result.data, status=status.HTTP_200_OK)


        except ClayfulException as e:

            return Response(e.code + ' ' + e.message, status=e.status)

        except Exception as e:
            print(e)
            return Response("알 수 없는 예외가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def get(self, request, result):
        try:

            Customer = Clayful.Customer
            options = {
                'customer': request.headers['Custom-Token'],
                'query': {
                },
            }

            options['query']['limit'] = 120
            # options['query']['limit']=3
            options['query']['page'] = request.GET.get('page', 1)

            result = Customer.list_coupons_for_me(options)

            headers = result.headers
            data = result.data

            for coupon in data:
                if coupon['expiresAt'] is not None:
                    coupon['expiresAt'] = coupon['expiresAt']['raw']
                    if datetime.datetime.strptime(coupon['expiresAt'],
                                                  '%Y-%m-%dT%H:%M:%S.%fZ') < datetime.datetime.utcnow():
                        options = {
                            'customer': request.headers['Custom-Token'],
                        }
                        Customer.delete_coupon_for_me(coupon['_id'], options)
                        continue

            return Response(data, status=status.HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response("알 수 없는 예외가 발생했습니다.", status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def delete(self, request, result):
        try:
            coupon_ids = request.data['coupon_ids']

            Customer = Clayful.Customer
            options = {
                'customer': request.headers['Custom-Token'],
                'query': {

                },
            }

            for coupon_id in coupon_ids:
                Customer.delete_coupon_for_me(coupon_id, options)

            return Response("총 {}개 삭제되었습니다".format(len(coupon_ids)), status=status.HTTP_200_OK)

        except ClayfulException as e:
            return Response(e.code, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response("알 수 없는 예외가 발생했습니다.", status=status.HTTP_400_BAD_REQUEST)
