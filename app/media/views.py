from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from influencer.views import is_influencer
from .models import *
from django.db.models import Q
from clayful import Clayful
from django.conf import settings
import json
import pprint
import requests
import datetime

class NoStreamKeyError(Exception):
    def __str__(self):
        return "스트림키를 생성해 주세요."

class NotEnoughDataError(Exception):
    def __str__(self):
        return "잘못된 입력입니다."

# 방송설정
@api_view(['POST'])
@is_influencer
def reserve_live(request, result):
    try:
        if result['meta']['Stream_url'] is None:
            raise NoStreamKeyError()
        # live 정보 저장
        #result['meta']['Stream_id'],
        new_media= MediaStream(
            title=request.data['title'],
            stream_url= result['meta']['Stream_url'],
            stream_id= "CMT7rhj5UGifi1yD3wijD9WqRFpyA0100KQo29YYEOCKs",
            product_id= request.data['product_id'],
            product_name= request.data['product_name'],
            influencer_name= result['name']['full'],
            influencer_id= result['_id'],
            description= request.data.get('description'),
            thumbnail_url= request.data.get('title'),
            started_at= request.data['started_at']
        )

        new_media.save()

        contents = {
            "success": {
                "message": "방송이 예약되었습니다."
            }
        }
        return Response(contents, status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        print(e)
        contents = {
            "error": {
                "message": e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 방송 수정

# 방송 취소

# 방송 종료



# mux callback 처리 (방송 시작, 방송 종료)
@api_view(['GET', 'POST'])
def mux_callback(request):
    # mux 암호화 확인 (추후에 추가 예정)
    try:
        if request.data['type'] == "video.live_stream.active":
            # Stream status -> live, create 시간 추가
            stream_id = request.data['object']['id']
            now_stream = MediaStream.objects.filter(Q(stream_id = stream_id) & Q(status='live'))
            now_stream.started_at = datetime.datetime.now().strftime()
            now_stream.status = 'live'
            pass
        elif request.data['type'] == "video.asset.live_stream_completed":
            # Stream status -> complete, Vod_url 저장, finish 시간 추가
            pass
        else:
            pass
    except Exception as e:
        print(e)




