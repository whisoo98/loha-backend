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
from django.core.exceptions import ObjectDoesNotExist
from product.views import set_raw
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
                'query': query
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
            # 스트림키가 존재하지 않는다면

            # Mux에서 스트림키 생성
            headers = {'Content-Type': 'application/json'}
            data = '{ "reduced_latency": true, "playback_policy": "public", "new_asset_settings": { "playback_policy": "public" } }'
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

            # Clayful meta정보에 저장
            Customer.update(result['_id'], payload)
            contents = {
                "success": {
                    'Stream_key': mux_data['data']['stream_key'],
                    'Stream_url': mux_data['data']['playback_ids'][0]['id'],
                    'Stream_id': mux_data['data']['id']
                }
            }
            return Response(contents)

        # 스트림키가 존재한다면 바로 반환
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


@api_view(['GET'])
@is_influencer
def get_stream_key_nevermind(request, result):  # 테스트용. 기존키 여부에 상관없이 새로 발급. MUX 문제 발생 가능. 서비스시 수정 필수.
    try:
        # Mux에서 스트림키 생성
        headers = {'Content-Type': 'application/json'}
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

        print(result)
        ready_medias = MediaStream.objects.filter(influencer_id=result['_id'])
        ready_medias.update(mux_livestream_playback_id=mux_data['data']['playback_ids'][0]['id'],
                            mux_livestream_id=mux_data['data']['id'])

        # Clayful meta정보에 저장
        Customer.update(result['_id'], payload)
        contents = {
            "success": {
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


# 스트림 키 재발급
@api_view(['GET'])
@is_influencer
def reset_stream_key(request, result):
    try:
        if result['meta']['Stream_key'] is None:
            # 스트림 키가 존재하지 않으면 에러
            contents = {
                "error": {
                    "message": "잘못된 요청입니다.",
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

        # 존재한다면 Mux로부터 재발급 요청
        mux_response = requests.post(
            f"https://api.mux.com/video/v1/live-streams/{result['meta']['Stream_id']}/reset-stream-key", auth=(
                getattr(settings, 'MUX_CLIENT_ID', None),
                getattr(settings, 'MUX_SECRET_KEY', None)))
        mux_data = mux_response.json()

        # Clayful에 수정
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
                'message': '재발급 되었습니다.',
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
                "Influencer_List": MediaSerializerforClient(live_list, many=True).data
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


# 인플루엔서 정보 수정
@api_view(['POST'])
@is_influencer
def update_info(request, result):
    try:
        Customer = Clayful.Customer
        options = {'customer': request.headers.get('Custom-Token')}
        payload = {
            'meta': {
                'description': request.data['description'],
                'tag': request.data['tag']
            }
        }
        Customer.update_me(payload, options)
        content = {
            "success": {
                "message": "변경 되었습니다."
            }
        }
        return Response(content, status=status.HTTP_202_ACCEPTED)

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


# 인플루엔서 한명 정보 가져오기
@api_view(['GET'])
def get_info(request):
    try:
        Customer = Clayful.Customer
        # 해당 id의 인플루엔서 불러오기
        # 일반고객을 불러오는 것을 방지하기 위해 인플루엔서 그룹만 불러온다.
        options = {
            'query': {
                'group': 'XU79MY58Q2C4',
                'ids': request.GET['influencer_id']
            }
        }
        res = Customer.list(options).data[0]
        is_live = MediaStream.objects.filter(Q(influencer_id=res['_id']) & Q(status='live'))

        # 현재 라이브 여부 정보 추가
        if not is_live:
            res['live_vod'] = 0
        else:
            res['live_vod'] = is_live[0].vod_id

        # 프론트가 보기 편한 format으로 변경
        res['Follower'] = res['meta']['Follower']['raw']
        res['description'] = res['meta']['description']
        res['tag'] = res['meta']['tag']
        res['thumbnail_url'] = res['meta']['thumbnail_url']
        if not res['avatar']:
            pass
        else:
            res['avatar'] = res['avatar']['url']

        # 과다한 정보 노출을 방지하기 위해 제거
        del (
            res['name'], res['address'], res['connect'], res['verified'], res['groups'], res['userId'], res['email'],
            res['gender'], res['birthdate'], res['mobile'], res['phone'], res['lastLoggedInAt'], res['createdAt'],
            res['updatedAt'], res['meta'])

        contents = {
            "success": {
                "data": res
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


# Influencer list (popular, new)
@api_view(['GET'])
def list_influencer(request, sort_by):
    try:
        Customer = Clayful.Customer
        # 모든 인플루엔서 불러오기
        # 인플루엔서 120명을 최대로 생각하고 구현.
        # 초과하면 다른 방향으로 구현해야됨.
        options = {
            'query': {
                #       'raw': True,
                'group': 'XU79MY58Q2C4',
                'limit': 120,
                'page': request.GET.get('page', 1),
                #        'fields': "_id,alias,avatar,country,name,meta.Follower"
            }
        }
        res = Customer.list(options).data
        # 기본 정렬이 만들어진 순서로 정렬
        # 과도한 개인 정보 삭제 및 프론트가 편한 format으로 변경
        for info in res:
            info['Follower'] = info['meta']['Follower']['raw']
            info['description'] = info['meta']['description']
            info['tag'] = info['meta']['tag']
            info['thumbnail_url'] = info['meta']['thumbnail_url']
            if not info['avatar']:
                pass
            else:
                info['avatar'] = info['avatar']['url']

            del (info['name'], info['address'], info['connect'], info['verified'], info['groups'], info['userId'],
                 info['email'], info['gender'], info['birthdate'], info['mobile'], info['phone'],
                 info['lastLoggedInAt'], info['createdAt'], info['updatedAt'], info['meta'])

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
        # 해당 인플루엔서 + 종료된 VOD
        # product_list만 불러온다.
        my_product = MediaStream.objects.filter(
            Q(influencer_id=request.GET['influencer_id']) & Q(status='completed')
        ).values_list('product_list', flat=True)

        # product_list 합친다.
        ids = ','.join(my_product)
        if not ids:
            contents = {
                'success': {
                    'message': '성공',
                    'product_list': []
                }
            }
            return Response(contents, status=status.HTTP_200_OK)

        # 해당 product_list 정보를 Clayful에서 불러온다.
        Product = Clayful.Product

        options = {
            'query': {
                'ids': ids
            }
        }

        res = Product.list(options)

        # 프론트가 편한 format으로 변경
        data = res.data
        for dict in data:
            dict = set_raw(dict)
        contents = {
            'success': {
                'message': '성공',
                'product_list': data
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


# 인플루엔서 방송 불러오기
@api_view(['GET'])
def get_my_vod(request):
    try:
        # 해당 인플루엔서가 생방송중 / 완료한 모든 방송 불러오기.
        my_vod = MediaSerializerforClient(
            MediaStream.objects.filter(
                Q(influencer_id=request.GET['influencer_id']) &
                (Q(status='live') | Q(status='completed') | Q(status='close'))
            ).order_by('-started_at'),
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


# 내가 예약한  방송 불러오기
@api_view(['GET'])
@is_influencer
def get_my_readyvod(request, result):
    try:
        my_vod = MediaSerializerforClient(
            MediaStream.objects.filter(Q(influencer_id=result['_id']) & Q(status='ready')).order_by('started_at'),
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
