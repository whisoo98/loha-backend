from django.shortcuts import render
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from clayful import Clayful
from user.views import require_login
import json


class VendorAPI(APIView):

    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    def post(self, request): # 입점사 생성
        try:
            Vendor = Clayful.Vendor
            payload = request.data['payload']
            options = {

            }
            result = Vendor.create(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:

            print(e.code)
            return Response("입점사를 생성하지 못했습니다.")

    def get(self, request):
        try:
            Vendor = Clayful.Vendor
            options = {
                'query': {

                },
            }
            result = Vendor.list(options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:

            print(e.code)
            return Response("입점사를 불러오지 못했습니다.")

    def delete(self, request):
        try:
            Vendor = Clayful.Vendor

            vendor_ids = request.data['vendor_ids']
            if vendor_ids is None:
                return Response("삭제할 입점사가 없습니다.")

            for vendor_id in vendor_ids:
                Vendor.delete(vendor_id)

            return Response("입점사가 삭제되었습니다.")
        except Exception as e:
            return Response("입점사 도중 에러가 발생하였습니다.")

    def put(self, request):
        try:
            Vendor = Clayful.Vendor
            payload = request.data['payload']
            vendor_id = request.data['vendor_id']
            if payload is None or vendor_id is None:
                return Response("정확한 정보를 입력하세요.")

            result = Vendor.update(vendor_id, payload)
            headers = result.headers
            data = result.data

            return Response(data)
        except Exception as e:

            print(e.code)
            return Response("입점사 수정이 완료되지 않았습니다.")


def get_vendor(request, vendor_id):
    try:
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

        Vendor = Clayful.Vendor

        options = {
            'query': {

            },
        }

        result = Vendor.get(vendor_id, options)

        headers = result.headers
        data = result.data

        return Response(data)

    except Exception as e:

        return Response("요청하신 입점사를 불러오지 못했습니다.")
