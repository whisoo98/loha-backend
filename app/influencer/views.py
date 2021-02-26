from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from clayful import Clayful
from django.conf import settings

# for vod
from media.models import *
from django.db.models import Q
from media.serializers import *
from chat.models import Room
from django.core.exceptions import ObjectDoesNotExist
import json
import pprint
import requests
import datetime

import urllib


# Create your views here.

class AuthorizationError(Exception):
    def __str__(self):
        return "접근 권한이 없습니다."


# 인플루엔서 확인 decorator
def is_influencer(func):
    def wrapper(request, *args, **kwargs):
        try:
            Customer = Clayful.Customer
            token = request.headers.get('Custom-Token')
            # 이름, 별명, 이메일, 그룹 불러오기
            query = {
                'raw': True,
                'fields': "userId,country,name,alias,email,groups,phone,meta,avatar"
            }
            options = {
                'customer': token,
                'query':query
            }
            kwargs['result'] = Customer.get_me(options).data

            if 'XU79MY58Q2C4' not in kwargs['result']['groups']:
                raise AuthorizationError()

        except Exception as e:
            print(e)
            try:
                print(e.code)
                print(e.message)
            except Exception as er:
                pass
            content = {
                "error": {
                    "message": "접근 권한이 없습니다."
                }
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        return func(request, *args, **kwargs)

    return wrapper


# 스트림 키 생성 및 가져오기
@api_view(['GET'])
@is_influencer
def get_stream_key(request, result):
    try:
        if not result['meta']['Stream_key']:
            headers = {'Content-Type': 'application/json'}
            # data = {
            #     "playback_policy": "public",
            #     "new_asset_settings": {
            #         "playback_policy": "public"
            #     }
            # }
            data = '{ "playback_policy": "public", "new_asset_settings": { "playback_policy": "public" } }'
            # "per_title_encode": True
            # "reduced_latency" : True -> 방송 딜레이 줄이기
            mux_response = requests.post('https://api.mux.com/video/v1/live-streams', headers=headers, data=data, auth=(
                getattr(settings, 'MUX_CLIENT_ID', None),
                getattr(settings, 'MUX_SECRET_KEY', None)))
            mux_data = mux_response.json()
            Customer = Clayful.Customer
            payload = {
                'meta': {
                    'Stream_key': mux_data['data']['stream_key'],
                    'Stream_url': mux_data['data']['playback_ids'][0]['id'],
                    'Stream_id': mux_data['data']['id']
                }
            }
            Customer.update(result['_id'], payload)

            Room.objects.create(room_streamer=result['_id'])

            contents = {
                "success": {
                    'Stream_key': mux_data['data']['stream_key'],
                    'Stream_url': mux_data['data']['playback_ids'][0]['id'],
                    'Stream_id': mux_data['data']['id']
                }
            }
            return Response(contents)
        print(result)
        contents = {
            "success": {
                'Stream_key': result['meta']['Stream_key'],
                'Stream_url': result['meta']['Stream_url'],
                'Stream_id': result['meta']['Stream_id']
            }
        }
        return Response(contents)
    except Exception as e:
        print(e)
        try:
            print(e.code)
            print(e.message)
        except Exception as er:
            pass
        contents = {
            "error": {
                "message": "잘못된 요청입니다.",
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 스트림 키 재발급
@api_view(['GET'])
@is_influencer
def reset_stream_key(request, result):
    try:
        if result['meta']['Stream_key'] is None:
            contents = {
                "error": {
                    "message": "잘못된 요청입니다.",
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

        mux_response = requests.post(f"https://api.mux.com/video/v1/live-streams/{result['meta']['Stream_id']}/reset-stream-key", auth=(
                getattr(settings, 'MUX_CLIENT_ID', None),
                getattr(settings, 'MUX_SECRET_KEY', None)))

        mux_data = mux_response.json()
        Customer = Clayful.Customer
        payload = {
            'meta': {
                'Stream_key': mux_data['data']['stream_key'],
                'Stream_url': mux_data['data']['playback_ids'][0]['id'],
                'Stream_id': mux_data['data']['id']
            }
        }
        Customer.update(result['_id'], payload)
        contents = {
            "success": {
                'message' : '재발급 되었습니다.',
                'Stream_key': mux_data['data']['stream_key'],
                'Stream_url': mux_data['data']['playback_ids'][0]['id'],
                'Stream_id': mux_data['data']['id']
            }
        }
        return Response(contents)
    except Exception as e:
        print(e)
        try:
            print(e.code)
            print(e.message)
        except Exception as er:
            pass
        contents = {
            "error": {
                "message": "잘못된 요청입니다.",
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# now live Influencer
@api_view(['GET'])
def live_influencer(request):
    try:
        live_list = MediaStream.objects.filter(status='live').distinct('influencer_id')
        contents = {
            "success": {
                "Influencer_List":MediaSerializerforClient(live_list, many=True).data
            }
        }
        return Response(contents)
    except ObjectDoesNotExist:
        contents = {
            "error": {
                "message": "잘못된 요청입니다.",
                "detail": "존재하지 않는 방송입니다.",
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        try:
            print(e.code)
            print(e.message)
        except Exception as er:
            pass
        content = {
            "error": {
                "message": "잘못된 요청입니다."
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)


# Influencer list (popular, new)
@api_view(['GET'])
def list_influencer(request, sort_by):
    try:
        Customer = Clayful.Customer

        options = {
            'query': {
         #       'raw': True,
                'group': 'XU79MY58Q2C4',
        #        'fields': "_id,alias,avatar,country,name,meta.Follower"
            }
        }

        # 만들어진 순서로 정렬
        res = Customer.list(options).data
        # 개인 정보 삭제
        for info in res:
            info['Follower'] = info['meta']['Follower']['raw']
            if not info['avatar']:
                pass
            else:
                info['avatar'] = info['avatar']['url']
            del(info['name'],info['address'],info['connect'],info['verified'],info['groups'], info['userId'], info['email'],info['gender'],info['birthdate'],info['mobile'],info['phone'],info['lastLoggedInAt'],info['createdAt'],info['updatedAt'], info['meta'])

        # 인기순 정렬
        if sort_by == 'popular':
            res = sorted(res, key=lambda r: r['Follower'], reverse=True)

        contents = {
            "success": {
                "Influencer_List": res
            }
        }
        return Response(contents)

    except Exception as e:
        print(e)
        try:
            print(e.code)
            print(e.message)
        except Exception as er:
            pass
        content = {
            "error": {
                "message": "잘못된 요청입니다."
            }
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# product of Influencer
@api_view(['GET'])
def get_my_product(request):
    try:
        my_product = MediaStream.objects.filter(
            Q(influencer_id=request.data['influencer_id']) & Q(status='completed')
        ).values_list('product_list', flat=True)
        ids = ','.join(my_product)
        if not ids:
            contents = {
                'success': {
                    'message': '성공',
                    'product_list': []
                }
            }
            return Response(contents, status=status.HTTP_200_OK)
        Product = Clayful.Product

        options = {
            'query': {
                'ids': ids
            }
        }

        res = Product.list(options)
        contents = {
            'success': {
                'message': '성공',
                'product_list': res.data
            }
        }
        return Response(contents, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'code': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
    pass


# 내 방송 불러오기
@api_view(['GET'])
def get_my_vod(request):
    try:
        my_vod = MediaSerializerforClient(
            MediaStream.objects.filter(influencer_id=request.data['influencer_id']).order_by('-started_at'),
            many=True)
        contents = {
            'success': {
                'message': '성공',
                'data': my_vod.data
            }
        }
        return Response(contents, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'code': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
