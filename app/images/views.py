from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from clayful import Clayful
from django.conf import settings
from user.views import require_login
import json
import requests
import datetime

class Images(APIView):

    # 내 이미지 가져오기
    @require_login
    def get(self, request, result):
        try:
            Image = Clayful.Image
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'model': 'Customer',
                    'application': 'avatar'
                }
            }
            res = Image.list_for_me(options)

            if not res.data:
                contents = {
                    "error": {
                        "message": "등록된 사진이 없습니다."
                    }
                }
                return Response(contents, status=status.HTTP_200_OK)

            contents = {
                "success": {
                    "data": res.data
                }
            }
            return Response(contents, status=status.HTTP_200_OK)


        except Exception as e:
            self.print_error(e)
            content = {
                'error': {
                    'message': '잘못된 요청입니다.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 이미지 추가 및 변경
    @require_login
    def post(self, request, result):
        try:
            Image = Clayful.Image
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'model': 'Customer',
                    'application': 'avatar'
                }
            }
            res = Image.list_for_me(options)
            # 아바타가 없을 때
            if result.data['avatar'] is None:
                payload = {
                    'model': (None, 'Customer'),
                    'application': (None, 'avatar'),
                    'file': ('image.jpg', request.data['file'], 'image/jpeg')
                }
                res = Image.create_for_me(payload, options)
                payload = {'avatar': res.data['_id']}
                Customer = Clayful.Customer
                Customer.update_me(payload, options)
                contents = {
                    'success': {
                        'message': '새로운 사진이 추가되었습니다.'
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)
            else:
                # 아바타가 존재
                payload = {'file': ('image.jpg', request.data['file'], 'image/jpeg')}
                Image.update_for_me(res.data[0]['_id'], payload, options)
                contents = {
                    'success': {
                        'message': '사진이 변경되었습니다.'
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            self.print_error(e)
            try:
                content = {
                    'error': {
                        'message': e.message,
                        'code': e.code
                    }
                }
            except Exception:
                content = {
                    'error': {
                        'message': '잘못된 요청입니다.'
                    }
                }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 이미지 삭제
    @require_login
    def delete(self, request, result):
        try:
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'model': 'Customer',
                    'application': 'avatar'
                }
            }
            Image = Clayful.Image
            Image.delete_for_me(result.data['avatar']['_id'], options)
            contents = {
                'success': {
                    'message': '사진이 삭제되었습니다.'
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            self.print_error(e)
            content = {
                'error': {
                    'message': '잘못된 요청입니다.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def print_error(request, e):
        print(e)
        try:
            print(e.model)
            print(e.method)
            print(e.code)
            print(e.status)
            print(e.message)
        except Exception as er:
            pass


# 인플루엔서 썸네일

class ThumbnailImages(APIView):

    # 내 이미지 가져오기
    def get(self, request):
        try:
            Image = Clayful.Image
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'model': 'WishList',
                    'application': None
                }
            }
            res = Image.list_for_me(options)

            if not res.data:
                contents = {
                    "error": {
                        "message": "등록된 사진이 없습니다."
                    }
                }
                return Response(contents, status=status.HTTP_200_OK)

            contents = {
                "success": {
                    "data": res.data
                }
            }
            return Response(contents, status=status.HTTP_200_OK)


        except Exception as e:
            self.print_error(e)
            content = {
                'error': {
                    'message': '잘못된 요청입니다.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 이미지 추가 및 변경
    @require_login
    def post(self, request, result):
        try:
            Image = Clayful.Image
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'model': 'Customer',
                    'application': 'avatar'
                }
            }
            res = Image.list_for_me(options)

            # 아바타가 없을 때
            if result.data['avatar'] is None:
                if not res.data:
                    payload = {
                        'model': (None, 'Customer'),
                        'application': (None, 'avatar'),
                        'file': ('image.jpg', request.data['file'], 'image/jpeg')
                    }
                    res = Image.create_for_me(payload, options)
                    payload = {
                        'meta': {
                            'thumbnail_url': res.data['url']
                        }
                    }
                    Customer = Clayful.Customer
                    Customer.update_me(payload, options)
                    contents = {
                        'success': {
                            'message': '새로운 썸네일이 추가되었습니다.'
                        }
                    }
                    return Response(contents, status=status.HTTP_202_ACCEPTED)
                payload = {'file': ('image.jpg', request.data['file'], 'image/jpeg')}
                Image.update_for_me(res.data[0]['_id'], payload, options)
                payload = {
                    'meta': {
                        'thumbnail_url': res.data['url']
                    }
                }
                Customer = Clayful.Customer
                Customer.update_me(payload, options)
                contents = {
                    'success': {
                        'message': '썸네일이 변경되었습니다.'
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)
            else:
                # 아바타가 존재
                thumb = ''
                for image in res.data:
                    if image['_id'] != result.data['avatar']['_id']:
                        thumb = image['_id']

                # 썸네일 사진이 아직 없을 때
                if thumb == '':
                    payload = {
                        'model': (None, 'Customer'),
                        'application': (None, 'avatar'),
                        'file': ('image.jpg', request.data['file'], 'image/jpeg')
                    }
                    res = Image.create_for_me(payload, options)
                    payload = {
                        'meta': {
                            'thumbnail_url': res.data['url']
                        }
                    }
                    Customer = Clayful.Customer
                    Customer.update_me(payload, options)
                    contents = {
                        'success': {
                            'message': '새로운 썸네일이 추가되었습니다.'
                        }
                    }
                    return Response(contents, status=status.HTTP_202_ACCEPTED)
            payload = {'file': ('image.jpg', request.data['file'], 'image/jpeg')}
            res = Image.update_for_me(thumb, payload, options)
            payload = {
                'meta': {
                    'thumbnail_url': res.data['url']
                }
            }
            Customer = Clayful.Customer
            Customer.update_me(payload, options)
            contents = {
                'success': {
                    'message': '썸네일이 변경되었습니다.'
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            self.print_error(e)
            try:
                content = {
                    'error': {
                        'message': e.message,
                        'code': e.code
                    }
                }
            except Exception:
                content = {
                    'error': {
                        'message': '잘못된 요청입니다.'
                    }
                }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 이미지 삭제
    @require_login
    def delete(self, request, result):
        try:
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'model': 'Customer',
                    'application': 'avatar'
                }
            }
            Image = Clayful.Image
            res = Image.list_for_me(options)
            if result.data['avatar'] is None and not res.data:
                Image.delete_for_me(res.data[0]['_id'], options)
                contents = {
                    'success': {
                        'message': '사진이 삭제되었습니다.'
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)

            thumb = ''
            for image in res.data:
                if image['_id'] != result.data['avatar']['_id']:
                    thumb = image['_id']
            if thumb != '':
                Image.delete_for_me(res.data[0]['_id'], options)
            contents = {
                'success': {
                    'message': '사진이 삭제되었습니다.'
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            self.print_error(e)
            content = {
                'error': {
                    'message': '잘못된 요청입니다.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def print_error(request, e):
        print(e)
        try:
            print(e.model)
            print(e.method)
            print(e.code)
            print(e.status)
            print(e.message)
        except Exception as er:
            pass
