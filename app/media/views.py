from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from influencer.views import is_influencer
from .models import *
from push.models import *
from push.views import *
from chat.models import *
from django.db.models import Q
from .serializers import *
from user.views import require_login
from clayful import Clayful, ClayfulException
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

# 방송 예약
@api_view(['POST'])
@is_influencer
def reserve_live(request, result):
    try:
        if result['meta']['Stream_url'] is None:
            raise NoStreamKeyError()
        # live 정보 저장
        #result['meta']['Stream_id'],
        new_media= MediaStream.objects.create(
            title=request.data['title'],
            stream_url= result['meta']['Stream_url'],
            stream_id= result['meta']['Stream_id'],
            product_id= request.data['product_id'],
            product_name= request.data['product_name'],
            influencer_name= result['name']['full'],
            influencer_id= result['_id'],
            description= request.data.get('description'),
            thumbnail_url= request.data.get('title'),
            started_at= request.data['started_at']
        )

        Room.objects.filter(room_streamer=result['_id']).all().delete()

        Room.objects.create(room_name=result['meta']['Stream_id'],
                            room_streamer=result['_id'])

        # 상품에 URL 추가
        contents = {
            "success": {
                "message": "방송이 예약되었습니다.",
                "data": MediaSerializer(new_media).data
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

# 방송 시작
@api_view(['POST'])
@is_influencer
def start_live(request, result):
    try:
        if result['meta']['Stream_url'] is None:
            raise NoStreamKeyError()

        # 라이브 상태 변경
        now_stream = MediaStream.objects.get(Q(pk=request.data['media_id']) & Q(influencer_id=result['_id']) & (Q(status='ready') | Q(status='live')))
        now_stream.save()
        info = {
            'influencer':result['alias'],
            'time': str(now_stream.started_at.hour) + ':' + str(now_stream.started_at.minute)
        }
        alarm_by_live(request.data['media_id'],info)
        alarm_by_influencer(result['_id'],info)
        contents = {
            "success": {
                "message": "방송이 시작되었습니다.",
                "data": MediaSerializer(now_stream).data
            }
        }
        return Response(contents, status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        contents = {
            "error": {
                "message": "잘못된 요청입니다."
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 방송 수정
@api_view(['POST'])
@is_influencer
def edit_my_vod(request, result):
    try:
        now_stream = MediaStream.objects.get(Q(pk=request.data['media_id']) & Q(influencer_id=result['_id']))
        now_stream.title = request.data.get('title') if request.data.get('title') is not None else now_stream.title
        now_stream.description = request.data.get('description') if request.data.get('description') is not None else now_stream.description
        now_stream.save()
        contents = {
            'success': {
                'message': '수정되었습니다.',
                'data': now_stream.data
            }
        }
        return Response(contents, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 방송 취소
@api_view(['Delete'])
@is_influencer
def delete_my_vod(request, result):
    try:
        now_stream = MediaStream.objects.get(Q(pk=request.data['media_id']) & Q(influencer_id=result['_id']))
        now_stream.delete()
        LiveAlarm.objects.filter(id=request.data['media_id']).all().delete()
        return Response("삭제되었습니다", status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response("알 수 없는 오류가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)


# 내 방송 불러오기
@api_view(['GET'])
@is_influencer
def get_my_vod(request, result):
    try:
        my_vod = MediaSerializer(MediaStream.objects.filter(influencer_id=result['_id']).order_by('-started_at'), many=True)
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



# 내가 좋아요 한 VOD 불러오기

# 상품에 추가된 VOD 불러오기

# VOD 좋아요
@require_login
def like_Vod(request, result):
    pass

# mux callback 처리 (방송 시작, 방송 종료)
@api_view(['GET', 'POST'])
def mux_callback(request):
    # mux 암호화 확인 (추후에 추가 예정)
    try:
        if request.data['type'] == "video.asset.live_stream_completed":
            # Stream status -> live, create 시간 추가
            stream_id = request.data['data']['live_stream_id']
            now_stream = MediaStream.objects.filter(Q(stream_id = stream_id) & Q(status='live')).order_by('started_at')[0]
            now_stream.vod_url = request.data['data']['playback_ids'][0]['id']
            now_stream.vod_id = request.data['data']['id']
            now_stream.finished_at = datetime.datetime.now()
            now_stream.status = 'completed'
            now_stream.save()

            return Response("completed")

        return Response("OK")
    except Exception as e:
        print(e)
        return Response('오류 발생')

class LiveAlarm(APIView):

    @require_login
    def get(self, request, result):
        try:
            contents = {
                "LiveAlarm_List": result.data['meta']['Live_id']
            }
            return Response(contents)
        except ClayfulException as e:
            print(e)
            return Response(e.code + ' ' + e.message, status=e.status)
        except Exception as e:
            print(e)
            return Response("알 수 없는 오류가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer
            if request.data.get('Live_id') in result.data['meta']['Live_id']: #Live예약 취소
                result.data['meta']['Live_id'].remove(request.data.get('Live_id'))
                payload = {
                    'meta': {
                        'Live_id': result.data['meta']['Live_id']
                    }
                }
                Customer.update(result.data['_id'], payload)
                return Response("라이브 예약이 취소되었습니다.", status=status.HTTP_202_ACCEPTED)
            #Live예약
            payload = {
                'meta': {
                    'Live_id': result.data['meta']['Live_id'] + [request.data.get('Live_id')]
                }
            }
            ##토큰을 저장해야함
            set_alarm_to_live(request.data.get('Live_id'),request.data['token'])

            Customer.update(result.data['_id'], payload)
            return Response("라이브 예약이 설정되었습니다.", status=status.HTTP_202_ACCEPTED)

        except ClayfulException as e:
            print(e)
            return Response(e.code + ' ' +e.message, status=e.status)
        except Exception as e:
            print(e)
            return Response('알 수 없는 오류가 발생하였습니다.',status=status.HTTP_400_BAD_REQUEST)

