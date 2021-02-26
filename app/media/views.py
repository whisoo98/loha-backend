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
from chat.models import *
from django.core.exceptions import ObjectDoesNotExist
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
        if result['meta']['Stream_key'] is None:
            raise NoStreamKeyError()
        avatar = ""
        if not result['avatar']:
            pass
        else:
            Image = Clayful.Image
            avatar = Image.get(result['avatar'], {'raw': True, 'fields' : 'url'}).data['url']

        # live 정보 저장
        new_media = MediaStream.objects.create(
            mux_livestream_playback_id=result['meta']['Stream_url'],
            mux_livestream_id=result['meta']['Stream_id'],
            title=request.data['title'],
            description=request.data['description'],
            influencer_name=result['name']['full'],
            influencer_id=result['_id'],
            influencer_thunmbnail = avatar,
            product_name=request.data['product_name'],
            product_price=request.data['product_price'],
            product_sale=request.data['product_sale'],
            product_brand=request.data['product_brand'],
            product_thumbnail=request.data['product_thumbnail'],
            product_list=request.data['product_list'],
            started_at=request.data['started_at']
        )

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
        if result['meta']['Stream_key'] is None:
            raise NoStreamKeyError()

        # 라이브 상태 변경
        now_stream = MediaStream.objects.get(
            vod_id=request.data['media_id'],influencer_id=result['_id'])

        now_stream.status = 'live'
        now_stream.save()

        # 상품에 VOD 추가
        stream_product = (now_stream.product_list).split(',')
        Product = Clayful.Product

        for product in stream_product:
            try:
                payload = {
                    "value": [
                        str(now_stream.vod_id)
                    ],
                    "unique": True
                }
                Product.push_to_metafield(product, "my_vod", payload)
            except Exception:
                print('error')
                continue

        # 알람 날리기
        # info = {
        #     'influencer': result['alias'],
        #     'time': str(now_stream.started_at.hour) + ':' + str(now_stream.started_at.minute)
        # }
        # alarm_by_live(request.data['media_id'], info)
        # alarm_by_influencer(result['_id'], info)
        contents = {
            "success": {
                "message": "방송이 시작되었습니다.",
                "data": MediaSerializer(now_stream).data
            }
        }
        return Response(contents, status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        contents = {
            'error': {
                'message': '존재하지 않는 방송입니다.'
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        contents = {
            "error": {
                "message": "잘못된 요청입니다.",
                "detail" : e.message,
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)


# 방송 수정
@api_view(['POST'])
@is_influencer
def edit_my_vod(request, result):
    try:
        now_stream = MediaStream.objects.get(
            vod_id=request.data['media_id'],influencer_id=result['_id'])

        avatar = ""
        if not result['avatar']:
            pass
        else:
            Image = Clayful.Image
            avatar = Image.get(result['avatar'], {'raw': True, 'fields': 'url'}).data['url']

        now_stream.mux_livestream_playback_id = result['meta']['Stream_url']
        now_stream.mux_livestream_id = result['meta']['Stream_id']
        now_stream.title = request.data['title']
        now_stream.description = request.data['description']
        now_stream.influencer_name = result['name']['full']
        now_stream.influencer_id = result['_id']
        now_stream.influencer_thunmbnail = avatar
        now_stream.product_name = request.data['product_name']
        now_stream.product_price = request.data['product_price']
        now_stream.product_sale = request.data['product_sale']
        now_stream.product_brand = request.data['product_brand']
        now_stream.product_thumbnail = request.data['product_thumbnail']
        now_stream.product_list = request.data['product_list']
        now_stream.started_at = request.data['started_at']

        now_stream.save()

        contents = {
            'success': {
                'message': '수정되었습니다.',
                'data': MediaSerializer(now_stream).data
            }
        }
        return Response(contents, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        contents = {
            "error": {
                "message": "잘못된 요청입니다.",
                "detail": "존재하지 않는 방송이거나 다른 인플루엔서의 방송입니다.",
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 방송 삭제
@api_view(['Delete'])
@is_influencer
def delete_my_vod(request, result):
    try:
        now_stream = MediaStream.objects.get(
            vod_id=request.data['media_id'],influencer_id=result['_id'])

        # MUX에서 영상 삭제
        if now_stream.mux_asset_id is not None:
            requests.delete(f'https://api.mux.com/video/v1/assets/{now_stream.mux_asset_id}', auth=(
                getattr(settings, 'MUX_CLIENT_ID', None),
                getattr(settings, 'MUX_SECRET_KEY', None)))

        # 상품에서 제거 -> table에 없으면 어차피 못 불러옴

        now_stream.delete()

        # 알람 삭제
        # LiveAlarm.objects.filter(Live_id=request.data['media_id']).all().delete()

        contents = {
            'success': {
                'message': '삭제 완료'
            }
        }
        return Response(contents, status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        contents = {
            'error': {
                'message': '존재하지 않는 방송입니다.',
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# Today byeolshow schedule
@api_view(["GET"])
def get_today_schedule(request):
    today_media = MediaSerializerforClient(
        MediaStream.objects.filter(Q(started_at__contains=datetime.date.today())).order_by('-started_at'), many=True)

    return Response(today_media.data)


# Tomorrow ~ byeolshow schedule
@api_view(["GET"])
def get_future_schedule(request):
    today_media = MediaSerializerforClient(
        MediaStream.objects.filter(Q(started_at__gt=datetime.date.today())).order_by('-started_at'), many=True)

    return Response(today_media.data)

# TODO 지금 핫한 방송
def get_hot_live(request):
    # TODO 인원수 불러오기 join 해서 order_by 할 예정
    # RoomUser.objects.filter(
    #     room_name=Room.objects.filter(room_name=self.room_name).all()[0]
    # ).count()
    today_media = MediaSerializer(
        MediaStream.objects.filter(Q(status='live')).order_by('-started_at'), many=True)

    return Response(today_media.data)


# TODO OPEN SPECIAL byeolshow

# TODO related byeolshow


# mux callback 처리 (방송 시작, 방송 종료)
@api_view(['GET', 'POST'])
def mux_callback(request):
    # TODO mux 암호화 확인
    try:
        print(request.data)
        if request.data['type'] == "video.asset.live_stream_completed":
            # Stream status -> live, create 시간 추가
            stream_id = request.data['data']['live_stream_id']
            now_stream = MediaStream.objects.get(mux_livestream_id=stream_id, status='live')
            now_stream.mux_asset_id = request.data['data']['id']
            now_stream.mux_asset_playback_id = request.data['data']['playback_ids'][0]['id']
            now_stream.finished_at = datetime.datetime.now()
            now_stream.status = 'completed'
            now_stream.save()
            return Response("completed")

        # TODO 오류 상황에 대한 예외 처리 필요할듯
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
            if request.data.get('_id') in result.data['meta']['Live_id']: #Live예약 취소
                result.data['meta']['Live_id'].remove(request.data.get('_id'))
                payload = {
                    'meta': {
                        'Live_id': result.data['meta']['Live_id']
                    }
                }
                Customer.update(result.data['_id'], payload)
                return Response("라이브 예약이 취소되었습니다.", status=status.HTTP_202_ACCEPTED)
            # Live예약
            payload = {
                'meta': {
                    'Live_id': result.data['meta']['Live_id'] + [request.data.get('_id')]
                }
            }
            ##토큰을 저장해야함
            set_alarm_to_live(request.data.get('_id'),request.data['token'])

            Customer.update(result.data['_id'], payload)
            return Response("라이브 예약이 설정되었습니다.", status=status.HTTP_202_ACCEPTED)

        except ClayfulException as e:
            print(e)
            return Response(e.code + ' ' + e.message, status=e.status)
        except Exception as e:
            print(e)
            return Response('알 수 없는 오류가 발생하였습니다.', status=status.HTTP_400_BAD_REQUEST)
