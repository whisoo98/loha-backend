from django.shortcuts import render

# Create your views here.

from rest_framework.views import Response
from rest_framework.views import APIView
from clayful import Clayful
import json


# @login_require
# 로그인 여부를 확인해 비로그인 시 실행 X --> 데코레이터 추가 필요
# 로그인 되어 있다고 가정
class WishList(APIView):
    # Clayful 초기화
    def __init__(self):
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    # WishList 불러오기
    def get(self, request):
        try:

            WishList = Clayful.WishList

            payload = {
                'name': 'default_wishlist',
                'description': None
            }

            options = {
               'customer': request.session.get('custom_token')
            }

            is_exist_wishlist = WishList.list_for_me(options)

            # wishlist가 없으면 생성
            # 첫 번째에만 실행
            if not is_exist_wishlist.data:
                is_exist_wishlist = WishList.create_for_me(payload, options)

            result = WishList.list_products_for_me(is_exist_wishlist.data[0]['_id'], options)
            return Response(result.data)

        except Exception as e:
            self.print_error(request, e)
            return Response("error")


    # WishList 추가
    # product_id String
    def post(self, request):
        WishList = Clayful.WishList

        payload = {
            'name': 'default_wishlist',
            'description': None
        }

        options = {
            'customer': request.session.get('custom_token')
        }

        is_exist_wishlist = WishList.list_for_me(options)

        # wishlist가 없으면 생성
        # 첫 번째에만 실행
        if not is_exist_wishlist.data:
            is_exist_wishlist = WishList.create_for_me(payload, options)

        # 아이템 추가
        # name
        payload = json.loads(request.body)

        result = WishList.add_item_for_me(is_exist_wishlist.data[0]['_id'], json.loads(request.body), options)
        return Response(result.data)

    # WishList 삭제
    # product_id String
    def delete(self, request):
        WishList = Clayful.WishList

        options = {
            'customer': request.session.get('custom_token')
        }

        is_exist_wishlist = WishList.list_for_me(options)
        result = WishList.delete_item_for_me(is_exist_wishlist.data[0]['_id'], request.data['product'], options)

        return Response(result.data)


    def print_error(self, request, e):
        print(e.is_clayful)
        print(e.model)
        print(e.method)
        print(e.status)
        print(e.headers)
        print(e.code)
        print(e.message)


'''
@api_view(['GET'])
def get_wishlist(request):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
        'customer': request.session.get('custom_token'),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:

        WishList = Clayful.WishList

        result = WishList.list_for_me()

        return Response(result.data)

    except Exception as e:

        # Error case
        print(e.code)


@api_view(['GET'])
def delete_wishlist(request):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
        'customer': request.session.get('custom_token'),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    try:
        WishList = Clayful.WishList

        WishList.delete_for_me('DGFTMR7Q78MJ')
        WishList.delete_for_me('MCMD85ERPYLX')
        WishList.delete_for_me('6RQF8FJ4Y7HL')
        result = WishList.delete_for_me('PTZ3J8AWVX36')


        return Response(result.data)

    except Exception as e:

        # Error case
        print(e.code)
'''
