from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from clayful import Clayful
from django.conf import settings
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
            token = request.headers['Authorization'].split()[1]
            # 이름, 별명, 이메일, 그룹 불러오기
            query = {
                'raw' : True,
                'fields': "userId,country,name,alias,email,groups,phone,meta"
            }
            options = {
                'customer': token,
                'query': query
            }

            kwargs['result'] = Customer.get_me(options).data
            if 'XU79MY58Q2C4' not in kwargs['result']['groups']:
                raise AuthorizationError()

        except Exception as e:
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
            content = {
                "error": {
                    "message": "접근 권한이 없습니다."
                }
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        return func(request, *args, **kwargs)
    return wrapper

# 스트림 키 가져오기
@api_view(['GET'])
@is_influencer
def get_stream_key(request, result):
    try:
        if result['meta']['Stream_key'] is None:
            headers = {'Content-Type': 'application/json'}
            data = '{ "playback_policy": "public", "new_asset_settings": { "playback_policy": "public" } }'
            mux_response = requests.post('https://api.mux.com/video/v1/live-streams', headers=headers, data=data, auth=(
            getattr(settings, 'MUX_CLIENT_ID', None),
            getattr(settings, 'MUX_SECRET_KEY', None)))
            mux_data = mux_response.json()
            Customer = Clayful.Customer
            payload ={
                'meta':{
                    'Stream_key': mux_data['data']['stream_key'],
                    'Stream_url': 'https://stream.mux.com/' + mux_data['data']['playback_ids'][0]['id'],
                    'Stream_id': mux_data['data']['id']
                }
            }
            Customer.update(result['_id'], payload)
            contents = {
                "success": {
                    'Stream_key': result['meta']['Stream_key'],
                    'Stream_url': result['meta']['Stream_url'],
                    'Stream_id': result['meta']['Stream_id']
                }
            }
            return Response(contents)
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
        content = {
            "error": {
                "message": "잘못된 요청입니다."
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 방송 시작하기





# Webhook 처리
# VOD 추가
@api_view(['GET','POST'])
def callback(request):
    print(request.data)
    # 방송시작 ( stream.active ) : 방송 상태 -> 알림?
    # 방송종료(stream.disconnected) : 방송 종료
    # video.asset.ready : 방송 종료 후 VOD 생성됨
    return Response('hihi')

# 스트리밍 시작
@is_influencer
def start_streaming(request):
    # 상품에 인플루엔서 추가
    # influencer에 상품 추가 ( 상품+날짜를 key로 해야될듯)
    # body에는 방송 제목, 상품, 날짜 등등 필요할듯
    pass
