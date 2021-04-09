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
            payload = (request.data)
            pprint.pprint(payload)
            img_list = []
            if len(request.FILES.getlist('images'))>0:
                img_list = request.FILES.getlist('images') #이미지 리스트
                img_payload = {
                    'model': (None, 'Review'),
                    'application': (None, 'images'),
                    #'file': ('image.jpg', request.data['images'], 'image/jpeg')
                }
                img_id = []
                for img in img_list:
                    img_payload['file'] = (
                        'image.jpg',
                        img,
                        'image/jpeg'
                    )
                    img_id.append(Image.create_for_me(img_payload,options).data['_id'])
                payload['images'] = img_id
            result = Review.create_for_me(payload, options)
            headers = result.headers
            data = result.data
            print(5)
            return Response(data)

        except ClayfulException as e:
            print(e)
            print(e.message)
            print(e.code)
            return Response(e.code+ ' ' + e.message, status=e.status)

        except Exception as e:
            print(e)
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

    def get(self, request, review_id):
        try:

            Review = Clayful.Review

            options = {
                'query': {
                    'fields':'-helped,-flagged,-rating,-totalComment,-commentedAt'
                },
            }

            result = Review.get_published(review_id, options)

            headers = result.headers
            data = result.data
            data['publishedAt']=data['publishedAt']['raw']
            data['createdAt']=data['createdAt']['raw']
            data['updatedAt']=data['updatedAt']['raw']
            data['product']['price']['original']=data['product']['price']['original']['raw']
            data['product']['price']['sale']=data['product']['price']['sale']['raw']
            data['product']['discount']['discounted']=data['product']['discount']['discounted']['raw']
            if data['product']['discount']['value'] is not None:
                data['product']['discount']['value']=data['product']['discount']['value']['raw']

            return Response(data)
        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            print(e)
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
            payload = request.data
            options = {
                'customer': request.headers['Custom-Token'],
            }

            before = Review.get_published(review_id, {}).data
            img_list = request.FILES.getlist('images')

            if img_list is None:
                res = Review.update_for_me(review_id,payload,options)
                return Response(res.data)
            else:
                before_img = before['images']
                for img in before_img:
                    Image.delete_for_me(img['_id'],options)

                after = []
                img_payload = {
                    'model': (None, 'Review'),
                    'application': (None, 'images'),
                }
                for img in img_list:
                    img_payload['file'] = (
                        'image.jpg',
                        img,
                        'image/jpeg'
                    )
                    after.append(Image.create_for_me(img_payload, options).data['_id'])

                payload['images'] = after
                result = Review.update_for_me(review_id, json.dumps(payload), options)

                headers = result.headers
                data = result.data

                return Response(data)

        except ClayfulException as e:
            return Response(e.code, status=e.status)

        except Exception as e:
            print(e)
            return Response("알 수 없는 오류가 발생하였습니다.", status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def review_list_published_api(request,product_id):
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
                'product':product_id,
                'limit': 120,
                #'limit': 3,
                'page': request.GET.get('page', 1),
                'fields':'-commentedAt,-flagged,-helped,-rating,-totalComment'
            },
        }
        result = Review.list_published(options)
        headers = result.headers
        data = result.data
        for review in data:
            review['publishedAt'] = review['publishedAt']['raw']
            review['createdAt'] = review['createdAt']['raw']
            review['updatedAt'] = review['updatedAt']['raw']
            review['product']['price']['original'] = review['product']['price']['original']['raw']
            review['product']['price']['sale'] = review['product']['price']['sale']['raw']
            review['product']['discount']['discounted'] = review['product']['discount']['discounted']['raw']
            if review['product']['discount']['value'] is not None:
                review['product']['discount']['value'] = review['product']['discount']['value']['raw']
        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        print(e)
        return Response("알 수 없는 오류가 발생하였습니다.")

@api_view(['GET'])
def review_list_published_for_me_api(request,customer_id):
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
                'fields':'-commentedAt,-flagged,-helped,-rating,-totalComment',
                'limit': 120,
                #'limit': 3,
                'page': request.GET.get('page', 1),
                'customer':customer_id,
            },
        }
        result = Review.list_published(options)
        headers = result.headers
        data = result.data
        for review in data:
            review['publishedAt'] = review['publishedAt']['raw']
            review['createdAt'] = review['createdAt']['raw']
            review['updatedAt'] = review['updatedAt']['raw']
            review['product']['price']['original'] = review['product']['price']['original']['raw']
            review['product']['price']['sale'] = review['product']['price']['sale']['raw']
            review['product']['discount']['discounted'] = review['product']['discount']['discounted']['raw']
            if review['product']['discount']['value'] is not None:
                review['product']['discount']['value'] = review['product']['discount']['value']['raw']
        return Response(data)

    except ClayfulException as e:
        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:
        print(e)
        return Response("알 수 없는 오류가 발생하였습니다.")