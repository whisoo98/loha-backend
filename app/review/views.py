from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
import pprint
from clayful import Clayful, ClayfulException
import json
import requests
import base64


class ReviewAPI(APIView):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    def post(self, request):
        try:
            Review = Clayful.Review
            Image = Clayful.Image
            options = {
                'customer': request.headers['Custom-Token'],
            }
            print(request.FILES)
            print(request.FILES['images'])
            print(dir(request.FILES['images']))
            print(request.FILES['images'][0].values)
            print(request.FILES['images'][0].items)
            print(request.FILES['images'][0].keys)

            payload = json.dumps(request.data['payload'])
            img_list = request.FILES #이미지 리스트
            pprint.pprint(request.data['images'])

            img_payload = {
                'model': (None, 'Review'),
                'application': (None, 'images'),
                'file': ('image.jpg', request.data['images'], 'image/jpeg')
            }
            print("!")
            pprint.pprint(img_list)
            pprint.pprint(request.files)
            img_id = []
            #res = Image.create_for_me(img_payload, options).data['_id']
            return Response("!")
            for img in img_list:
                print(img)
                img_payload['file'] = (
                    'image.jpg',
                    open('./path/to/image.jpg', 'rb'),
                    'image/jpeg'
                )
                pprint.pprint(img_payload)
                #img_id.append(Image.create_for_me(img_payload,options).data['_id'])
            print("!")

            payload['images'] = img_id

            result = Review.create_for_me(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def get(self, request, review_id):
        try:

            Review = Clayful.Review

            options = {
                'query': {

                },
            }

            result = Review.get_published(review_id, options)

            headers = result.headers
            data = result.data

            return Response(data)
        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        try:
            Review = Clayful.Review
            options = {
                'customer': request.headers['Custom-Token'],
            }

            result = Review.delete_for_me(review_id, options)
            headers = result.headers
            data = result.data

            return Response("삭제가 완료되었습니다.")

        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def put(self, request, review_id):
        try:
            Review = Clayful.Review
            Image = Clayful.Image
            payload = json.dumps(request.data['payload'])
            options = {
                'customer': request.headers['Custom-Token'],
            }

            img_list = request.data['images']

            before = Review.get_published(review_id, {
                'customer': request.headers['Custom-Token'],
                'field': 'images'
            }).data

            for img in before:
                Image.delete_for_me(img,options)

            after = []
            img_payload = {
                'model': 'Review',
                'application': 'images'
            }
            for img in img_list:
                img_payload['file'] = img
                after.append(Image.create_for_me(img_payload, options))

            payload['images'] = after
            result = Review.update_for_me(review_id, payload, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def review_list_published_api(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Review = Clayful.Review

        options = {
            'query': {
                'product':request.data['product_id']
            },
        }
        result = Review.list_published(options)
        headers = result.headers
        data = result.data

        return Response(data)

    except ClayfulException as e:
        return Response(e.code, status=e.status)

    except Exception as e:
        return Response("알 수 없는 오류가 발생하였습니다.")

