from django.shortcuts import render

# Create your views here.

from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from clayful import Clayful
from user.views import require_login
import json

# 좋아요 상품 목록 확인
class ProductWishList(APIView):
    # Clayful 초기화
    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    # ProductWishList 불러오기
    @require_login
    def get(self, request, result):
        try:
            WishList = Clayful.WishList
            options = {'customer': request.headers.get('custom_token')}
            result = WishList.list_for_me(options)

            idx = -1
            for i in range(3):
                if result.data[i]['name'] == 'product_wishlist':
                    idx=i
                    break
            query = {
                'raw': True,
                'limit': 15,
                'page': request.GET['page'],
                'fields': 'brand,bundled,bundles,vendor,thumbnail'
            }
            options['query'] = query
            result2 = WishList.list_products_for_me(result.data[idx]['_id'], options)
            return Response(result2.data)

        except Exception as e:
            self.print_error(e)
            content = "잘못된 요청"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # WishList 추가
    @require_login
    def post(self, request, result):
        try:
            WishList = Clayful.WishList
            options = {'customer': request.headers.get('custom_token')}
            result = WishList.list_for_me(options)
            # 상품 추가
            payload = {'product': request.data['product']}
            WishList.add_item_for_me(result.data[0]['_id'], payload, options)
            content = '추가 완료'
            return Response(content, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            self.print_error(e)
            content = "잘못된 요청"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # WishList 삭제
    @require_login
    def delete(self, request, result):
        try:
            WishList = Clayful.WishList
            options = {'customer': request.headers.get('custom_token')}
            result = WishList.list_for_me(options)
            result = WishList.delete_item_for_me(result.data[0]['_id'], request.data['product'], options)
            return Response(result.data)
        except Exception as e:
            self.print_error(e)
            content = "잘못된 요청"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def print_error(request, e):
        print(e)
        try:
            print(e.is_clayful)
            print(e.model)
            print(e.method)
            print(e.status)
            print(e.headers)
            print(e.code)
            print(e.message)
        except Exception as er:
            pass

