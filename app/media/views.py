from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from influencer.views import is_influencer
from .models import *
from push import models
from push.models import *
from push.views import *
from push import models
from chat.models import *
import hmac
import hashlib
from django.db.models import Q
from .serializers import *
from user.views import require_login
from clayful import Clayful, ClayfulException
from chat.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
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

def add_push_info(vods):
    for vod in vods:
         vod['push_count'] = LiveAlarm.objects.filter(vod_id=str(vod['vod_id'])).count()
    return vods

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
            notice=request.data['notice'],
            description=request.data['description'],
            influencer_name=result['name']['full'],
            influencer_id=result['_id'],
            influencer_thunmbnail = avatar,
            product_id=request.data['product_id'],
            product_name=request.data['product_name'],
            product_price=request.data['product_price'],
            product_sale=request.data['product_sale'],
            product_brand=request.data['product_brand'],
            product_thumbnail=request.data['product_thumbnail'],
            product_list=','.join(request.data['product_list']),
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
        now_stream.notice = request.data['notice']
        now_stream.description = request.data['description']
        now_stream.influencer_name = result['name']['full']
        now_stream.influencer_id = result['_id']
        now_stream.influencer_thunmbnail = avatar
        now_stream.product_id = request.data['product_id'],
        now_stream.product_name = request.data['product_name']
        now_stream.product_price = request.data['product_price']
        now_stream.product_sale = request.data['product_sale']
        now_stream.product_brand = request.data['product_brand']
        now_stream.product_thumbnail = request.data['product_thumbnail']
        now_stream.product_list=','.join(request.data['product_list'])
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

        # TODO 알람 삭제
        # unset_alarm_to_live(vod_id = request.data['media_id'])
        
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


# 방송 종료
@api_view(['POST'])
@is_influencer
def end_vod(request, result):
    try:
        now_stream = MediaStream.objects.get(
            vod_id=request.data['media_id'], influencer_id=result['_id'])
        now_stream.status = 'close'
        now_stream.save()


        contents = {
            'success': {
                'message': '방송 종료'
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

# 오늘 방송 일정 불러오기 live
@api_view(["GET"])
def get_today_live_schedule(request):
    try:
        today_media = MediaSerializerforClient(
            MediaStream.objects.filter(
                Q(status='live')
            ).order_by('started_at'), many=True)
        res = add_push_info(today_media.data)
        return Response(res)
    except ObjectDoesNotExist:
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 오늘 방송 일정 불러오기 ready
@api_view(["GET"])
def get_today_ready_schedule(request):
    try:
        today_media = MediaSerializerforClient(
            MediaStream.objects.filter(
                Q(started_at__gte=datetime.date.today()) & Q(status='ready')
            ).order_by('started_at')[:10], many=True)
        res = add_push_info(today_media.data)
        return Response(res)
    except ObjectDoesNotExist:
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)


# 미래 방송 일정 불러오기
@api_view(["GET"])
def get_future_schedule(request):
    try:
        today_media = MediaSerializerforClient(
            MediaStream.objects.filter(Q(started_at__gt=datetime.date.today()) & Q(status='ready')).order_by('started_at'), many=True)
        res = add_push_info(today_media.data)
        contents = {
            'success': {
                'live_list': res
            }
        }
        return Response(contents)
    except ObjectDoesNotExist:
        contents = {
            'success': {
                'ready_list': []
            }
        }
        return Response(contents)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 아직 시작하지 않은 모든 방송 불러오기
@api_view(["GET"])
def get_ready_schedule(request):
    try:
        today_media = MediaSerializerforClient(
            MediaStream.objects.filter(status='ready').order_by('started_at'), many=True)
        res = add_push_info(today_media.data)
        return Response(res)
    except ObjectDoesNotExist:
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

# 지금 핫한 방송(누적 시청자순)
@api_view(["GET"])
def get_hot_live(request):
    try:
        hot_media = MediaSerializerforClient(
            MediaStream.objects.filter(Q(status='live')).order_by('-vod_view_count'), many=True)
        return Response(hot_media.data)
    except ObjectDoesNotExist:
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
# 하나의 방송 불러오기
@api_view(["GET"])
def get_live(request):
    try:
        now_media = MediaStream.objects.get(pk=int(request.GET['media_id']))
        Product = Clayful.Product

        options = {
            'query': {
                'ids': now_media.product_list
            }
        }
        res = MediaSerializerforClient(now_media).data

        res['product_list'] = Product.list(options).data
        contents = {
            'success': res
        }
        return Response(contents, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        contents = {
            'error': {
                'message': '존재하지 않는 방송입니다.'
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


# TODO OPEN SPECIAL byeolshow

# related byeolshow (같은 콜렉션 상품들의 영상)
@api_view(["GET"])
def get_related(request):
    try:
        Product = Clayful.Product
        print("hihi")
        options = {
            'query': {
                'raw': True,
                'fields': 'meta',
                'collection': request.GET['collection_id'],
                'limit': 120,
            }
        }

        result = Product.list(options).data
        related_vod_list = []
        cnt = 0
        for product in result:
            try:
                related_vod_list.append(product['meta']['my_vod'][1])
                cnt+=1
            except:
                pass
            if cnt > 5 :
                break

        my_vod = MediaSerializerforClient(
            MediaStream.objects.filter(vod_id__in=related_vod_list).order_by('-vod_view_count')
            , many=True)
        return Response(my_vod.data)
    except ObjectDoesNotExist:
        return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        contents = {
            'error': {
                'message': '알 수 없는 오류',
                'detail': e
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)



# mux callback 처리 (방송 시작, 방송 종료)
@api_view(['GET', 'POST'])
def mux_callback(request):

    # try:
    #     # MUX 검증
    #     muxSig = request.headers.get('Mux-Signature')
    #     muxSigArray = muxSig.split(',')
    #     muxTimestamp = muxSigArray[0].replace('t=', '')
    #     muxHash = muxSigArray[1].replace('v1=', '')
    #     payload = f'{muxTimestamp}.{request.body}'
    #     print(payload)
    #     ourSignature = hmac.new(
    #         'sankq55952bg4018e8g40ukto65ou1on'.encode('utf-8'),
    #         msg=payload.encode('utf-8'),
    #         digestmod=hashlib.sha256
    #     ).hexdigest()
    #     print(ourSignature)
    #     print(muxHash)
    #     if muxHash!=ourSignature:
    #         return Response("unauthorized", status=HTTP_401_UNAUTHORIZED)
    #     return Response("done")
    # except Exception as e:
    #     print(e)
    #     return Response("unauthorized", status=HTTP_401_UNAUTHORIZED)
    try:
        print(request.data)
        if request.data['type'] == "video.asset.live_stream_completed":
            # Stream status -> live, create 시간 추가
            stream_id = request.data['data']['live_stream_id']
            now_stream = MediaStream.objects.get(mux_livestream_id=stream_id, status='close')
            now_stream.mux_asset_id = request.data['data']['id']
            now_stream.mux_asset_playback_id = request.data['data']['playback_ids'][0]['id']
            now_stream.finished_at = datetime.datetime.now()
            now_stream.status = 'completed'
            now_stream.save()

            # TODO 알람 삭제
            #unset_alarm_to_live(vod_id=now_stream.void_id)
            return Response("completed")

        # TODO 오류 상황에 대한 예외 처리 필요할듯
        
        return Response("OK")
    except ObjectDoesNotExist:
        contents = {
            'error': {
                'message': '존재하지 않는 방송입니다.'
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
    except MultipleObjectsReturned:
        contents = {
            'error': {
                'message': '라이브 중인 방송이 2개 이상입니다.'
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


class Alarm(APIView):
    @require_login
    def post(self, request, result):
        pprint.pprint(result.data)

        try:
            Live_id = str(request.data['_id'])
            Customer = Clayful.Customer
            # Live예약 취소
            if Live_id in result.data['meta']['Live_id']:
                Customer.pull_from_metafield(result.data['_id'],'Live_id',{'value':Live_id},{})
                content = {
                    'status': False,
                    'message': "라이브 예약이 취소되었습니다."
                }
                return Response(content, status=status.HTTP_202_ACCEPTED)
            # Live예약

            ##토큰을 저장해야함
            #set_alarm_to_live(request.data.get('_id'),request.data['token'])

            Customer.push_to_metafield(result.data['_id'],'Live_id',{'value':Live_id,'unique':True},{})
            content = {
                'status':True,
                'message':"라이브 예약이 설정되었습니다."
            }
            return Response(content, status=status.HTTP_202_ACCEPTED)

        except ClayfulException as e:
            print(e)
            return Response(e.code + ' ' + e.message, status=e.status)
        except Exception as e:
            print(e)
            return Response('알 수 없는 오류가 발생하였습니다.', status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def get(self, request, result):
        try:

            Live_list = result.data['meta']['Live_id'][1:]

            media_list = MediaSerializerforClient(
                MediaStream.objects.filter(Q(vod_id__in=Live_list) & Q(status='ready') & Q(started_at__gt=datetime.datetime.now())).order_by('started_at'), many=True
            ).data
            return Response(media_list, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            contents = {
                'error': {
                    'message': '존재하지 않는 방송입니다.'
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)
        except ClayfulException as e:
            print(e)
            return Response(e.code + ' ' + e.message, status=e.status)
        except Exception as e:
            print(e)
            return Response("알 수 없는 오류가 발생하였습니다.", status=status.HTTP_400_BAD_REQUEST)

# 누적 시청자수 증가
@api_view(['GET', 'POST'])
def add_view(request):
    try:
        now_stream = MediaStream.objects.get(
            vod_id=request.data['media_id'])

        now_stream.vod_view_count +=1
        now_stream.save()
        contents = {
            'success': {
                'message': '완료',
                'media_id': now_stream.vod_id,
                'now_view_count' : now_stream.vod_view_count
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
