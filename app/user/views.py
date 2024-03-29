import datetime
import re

import requests
from clayful import Clayful
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.views import Response

from media.serializers import *
from push.views import *
from user.models import UserToken


# 로그인 확인 decorator
def require_login(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            Customer = Clayful.Customer
            # token = request.headers['Authorization'].split()[1]
            # 이름, 별명, 이메일, 그룹 불러오기
            options = {'customer': request.headers.get('Custom-Token')}
            kwargs['result'] = Customer.get_me(options)
        except Exception as e:
            print(e)
            try:
                print(e.code)
                print(e.message)
            except Exception as er:
                pass
            content = {
                'error': {
                    'message': '로그인 후 이용해 주세요.'
                }
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        return func(self, request, *args, **kwargs)

    return wrapper


# 회원 active 여부 확인
def is_active(token):
    try:
        Customer = Clayful.Customer

        options = {
            'customer': token
        }

        result = Customer.get_me(options)

        return result.data['meta']['active']


    except Exception as e:
        print(e.code)


class Active(APIView):
    def get(self, request):
        try:
            Customer = Clayful.Customer
            options = {
                'customer': request.headers.get('Custom-Token'),
                'query': {
                    'fields': 'meta.active'
                },
            }

            result = Customer.get_me(options)

            contents = {
                "active": result.data['meta']['active']
            }

            return Response(contents)
        except Exception as e:
            content = {
                'error': {
                    'message': str(e)
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class Unsubcribe(APIView):
    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer
            payload = {
                'meta': {
                    'active': False,
                }
            }
            options = {'customer': request.headers.get('Custom-Token')}

            Customer.update_me(payload, options)

            contents = {
                "success": {
                    "active": False
                }
            }
            return Response(contents)
        except Exception as e:
            content = {
                'error': {
                    'message': str(e)
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


# 닉네임 중복 확인
@api_view(['POST'])
def check_name(request):
    try:
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })
        Customer = Clayful.Customer

        options = {
            'query': {
                'raw': True,
                'fields': 'name,country',
                'firstName': request.data['alias']
            }
        }

        result = Customer.list(options).data

        if not result:
            content = {
                'success': {
                    'message': '사용 가능한 닉네임입니다.'
                }
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                'error': {
                    'message': '사용 불가능한 닉네임입니다.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        content = {
            'error': {
                'message': '오류 발생'
            }
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# Clayful 초기화 decorator
def Init_Clayful(func):
    def wrapper(*args, **kwargs):
        # Clayful 초기화
        try:
            Clayful.config({
                'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
                'language': 'ko',
                'currency': 'KRW',
                'time_zone': 'Asia/Seoul',
                'debug_language': 'ko',
            })
        except Exception as e:
            print(e)
            content = {
                'error': {
                    'message': 'Clay Error'
                }
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        # 해당 함수 실행
        ret = func(*args, **kwargs)
        return ret

    return wrapper


# 회원가입, 탈퇴, 정보 수정, 정보 불러오기
class User(APIView):

    # Clayful 초기화
    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    # 현재 회원정보 출력
    @require_login
    def get(self, request, result):
        res = result.data
        # 프론트가 요구한 format으로 전환
        res['name'] = res['name']['full']
        res['unipass_number'] = res['meta']['unipass_number']
        for group in res['groups']:
            if group['_id'] == 'XU79MY58Q2C4':
                res['influencer'] = True
                break
            else:
                res['influencer'] = False
        del (res['connect'], res['verified'], res['gender'], res['groups'], res['birthdate'], res['phone'],
             res['lastLoggedInAt'], res['createdAt'], res['updatedAt'], res['meta'])
        if res['address']['primary'] is None:
            res['address'] = {
                "primary": {
                    "name": {
                        "first": "",
                        "last": "",
                        "full": ""
                    },
                    "mobile": "",
                    "phone": "",
                    "country": "",
                    "state": "",
                    "city": "",
                    "address1": "",
                    "address2": "",
                    "postcode": "",
                    "company": ""
                }
            }
        return Response(res)

    # 회원가입
    def put(self, request):
        try:
            Customer = Clayful.Customer
            if request.data['password'] != request.data['re_password']:
                content = "비밀번호가 일치하지 않습니다."
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            payload = {
                'groups': ['ZZ9HGQBGPLTA'],  # 일반고객으로 추가
                'userId': request.data['userId'],
                'email': request.data['email'],
                'password': request.data['password'],
                'name': {
                    'first': request.data['alias'],
                    'full': request.data['name']
                },
                'alias': request.data['alias'],
                'mobile': None if request.data['mobile'] == "" else request.data['mobile'],
            }
            if request.data['address']['primary']['name']['full'] != "":
                payload['address'] = {
                    "primary": request.data['address']['primary']
                }
            result = Customer.create(payload)
            # wishlist 생성
            self.make_wishlist(Clayful.WishList, result.data['_id'])
            content = {
                'success': {
                    'message': '회원가입 완료'
                }
            }
            return Response(content, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            self.print_error(e)
            try:
                if 'duplicated' in e.code:
                    content = {
                        'error': {
                            'message': '이미 가입된 아이디/이메일 입니다.'
                        }
                    }
                    content = {
                        'error': {
                            'message': e.message,
                            'code': e.code
                        }
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    content = {
                        'error': {
                            'message': '허용되지 않는 입력입니다.'
                        }
                    }
                    content = {
                        'error': {
                            'message': e.message,
                            'code': e.code
                        }
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except Exception as err:
                content = {
                    'error': {
                        'message': '정보를 모두 입력해 주세요.'
                    }
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정
    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer
            options = {'customer': request.headers.get('Custom-Token')}
            # 네이티브 로그인은 비밀번호 필요
            if not result.data['social']:
                # 로그인 정보 수정 (이메일, 비밀번호)
                if request.data.get('old_password') is not None:
                    payload = {
                        'password': request.data['old_password'],
                        'credentials': {
                            'userId': result.data['userId'],
                            'email': result.data['email'] if request.data['email'] == "" else request.data['email'],
                            'password': request.data['old_password'] if request.data['new_password'] == "" else
                            request.data['new_password'],
                        }
                    }
                    Customer.update_credentials_for_me(payload, options)
                else:
                    content = {
                        'error': {
                            'message': '비밀번호 입력해 주세요.'
                        }
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            # 개인 정보 수정 (이름, 번호, 별명)

            payload = {
                'name': {
                    'first': None if request.data['alias'] == "" else request.data['alias'],
                    'full': None if request.data['name'] == "" else request.data['name']
                },
                'alias': request.data['alias'],
                'mobile': None if request.data['mobile'] == "" else request.data['mobile'],
                'meta': {
                    'unipass_number': request.data['unipass_number']
                }
            }

            if request.data['address']['primary']['city'] != '':
                payload['address'] = {
                    "primary": request.data['address']['primary'],
                    "secondaries": request.data['address']['secondaries']
                }

            Customer.update_me(payload, options)
        except Exception as e:
            self.print_error(e)
            if 'duplicated' in e.code:
                # content = "이미 가입된 아이디 입니다."
                content = {
                    'error': {
                        'message': e.message,
                        'code': e.code
                    }
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            elif 'password' in e.code:
                # content = "잘못된 비밀번호입니다."  # 로그인 정보 변경시
                content = {
                    'error': {
                        'message': e.message,
                        'code': e.code
                    }
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {
                    'error': {
                        'message': e.message,
                        'code': e.code
                    }
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        content = {
            'success': {
                'message': '변경 완료.'
            }
        }
        return Response(content, status=status.HTTP_202_ACCEPTED)

    # 회원 탈퇴
    @require_login
    def delete(self, request, result):
        try:
            Customer = Clayful.Customer
            options = {'customer': request.headers.get('Custom-Token')}
            Customer.delete_me(options)
        except Exception as e:
            self.print_error(e)
            content = {
                'error': {
                    'message': e.massage
                }
            }

            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        content = {
            'success': {
                'message': '탈퇴 완료.'
            }
        }
        return Response(content, status=status.HTTP_202_ACCEPTED)

    def print_error(request, e):
        print(e)
        try:
            print(e.model)
            print(e.method)
            print(e.code)
            print(e.message)
        except Exception as er:
            pass

    def make_wishlist(request, WishList, customer):
        payload = {
            'customer': customer,
            'name': 'product_wishlist',
            'description': None
        }
        WishList.create(payload)


# 네이티브 로그인, 로그아웃 with Clayful
class Auth(APIView):
    def __init__(self):
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    # 로그인 함수
    def post(self, request):
        try:
            Customer = Clayful.Customer

            # body에서 'userId', 'password' 필요
            payload = {
                'userId': request.data['userId'],
                'password': request.data['password'],
            }
            response = Customer.authenticate(payload)

            # header에 정보 전송
            header = {'Custom-Token': response.data['token']}

            if not is_active(response.data['token']):
                content = {
                    'error': {
                        'message': '탈퇴한 회원입니다.'
                    }
                }
                return Response(content, status=status.HTTP_409_CONFLICT)

            content = {
                'success': {
                    'message': '로그인 완료.'
                }
            }
            return Response(content, headers=header)

        except Exception as e:
            self.print_error(e)
            content = {
                'error': {
                    'message': '잘못된 입력입니다.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃 함수
    def get(self, request):
        if request.headers.get('kakao_token') is not None:
            token = request.headers.get('kakao_token')
            header = {'Authorization': f'Bearer {token}'}
            requests.get("https://kapi.kakao.com//v1/user/logout", headers=header)

        content = "로그아웃 성공"
        return Response(content)

    def print_error(request, e):
        print(e)
        try:
            print(e.model)
            print(e.method)
            print(e.code)
            print(e.message)
        except Exception as er:
            pass


# kakao 소셜 로그인

# 코드 요청
@api_view(['GET'])
def kakao_login(request):
    app_rest_api_key = getattr(settings, 'KAKAO_REST_API', None)
    local_host = "https://www.byeolshowco.com/"
    # local_host = "http://127.0.0.1:8000/"
    redirect_uri = local_host + "user/auth/kakao/callback/"
    state = hash(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    request.session['my_state'] = state
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code&state={state}")


# 토큰 요청 및 정보 처리
@api_view(['GET', 'POST'])
def kakao_callback(request):
    try:
        app_rest_api_key = getattr(settings, 'KAKAO_REST_API', None)
        local_host = "https://www.byeolshowco.com/"
        # local_host = "http://127.0.0.1:8000/"
        redirect_uri = local_host + "user/auth/kakao/callback/"
        user_token = request.query_params['code']
        state = request.query_params['state']
        my_state = str(request.session['my_state'])
        request.session.pop('my_state')
        # CSRF 방지
        if state != my_state:
            content = "잘못된 접근"
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        # 토큰 획득
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )

        token_response = token_request.json()
        error = token_response.get("error", None)

        if error is not None:
            print(token_response)
            content = "로그인 실패"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 카카오 토큰, 저장 안함
        kakao_access_token = token_response.get("access_token")

        @Init_Clayful
        def kakao_to_clayful():
            Customer = Clayful.Customer
            payload = {'token': kakao_access_token}
            result = Customer.authenticate_by_3rd_party('kakao', payload)
            headers = {'Authorization': f'Bearer {kakao_access_token}'}
            response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
            user_data = response.json()

            update_payload = {
                'alias': user_data['kakao_account']['profile']['nickname'],
                'name': {
                    'first': user_data['kakao_account']['profile']['nickname'],
                    'full': user_data['kakao_account']['profile']['nickname']
                },
                'groups': ['ZZ9HGQBGPLTA']
            }
            if user_data['kakao_account']['has_email']:
                update_payload['email'] = user_data['kakao_account']['email']
            if user_data['kakao_account']['phone_number']:
                update_payload['mobile'] = user_data['kakao_account']['phone_number']
            # 가입과 동시 로그인
            if result.data['action'] == 'register':
                WishList = Clayful.WishList
                payload = {
                    'customer': result.data['customer'],
                    'name': 'product_wishlist',
                    'description': None
                }
                WishList.create(payload)

                payload = {'token': kakao_access_token}
                result = Customer.authenticate_by_3rd_party('kakao', payload)
                Customer.update(result.data['customer'], update_payload)

            return result

        result = kakao_to_clayful()

        content = f"<h1 style='color:#ffffff'>{result.data['token']}</h1>"
        header = {'Custom-Token': result.data['token']}
        return HttpResponse(content)
    except Exception as e:
        print(e)
        content = {
            'error': {
                'message': '로그인에 실패하였습니다.'
            }
        }
        try:
            content['error']['detail'] = e.message
            print(e.is_clayful)
            print(e.model)
            print(e.method)
            print(e.status)
            print(e.headers)
            print(e.code)
            print(e.message)
        except Exception as er:
            pass
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def kakao_token(request):
    try:
        kakao_access_token = request.data['kakao_access_token']
        Customer = Clayful.Customer
        payload = {'token': kakao_access_token}
        result = Customer.authenticate_by_3rd_party('kakao', payload)
        headers = {'Authorization': f'Bearer {kakao_access_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
        user_data = response.json()

        update_payload = {
            'alias': user_data['kakao_account']['profile']['nickname'],
            'name': {
                'first': user_data['kakao_account']['profile']['nickname'],
                'full': user_data['kakao_account']['profile']['nickname']
            },
            'groups': ['ZZ9HGQBGPLTA']
        }
        if user_data['kakao_account']['has_email']:
            update_payload['email'] = user_data['kakao_account']['email']
        phone_number_raw = user_data['kakao_account'].get('phone_number', None)
        if phone_number_raw:
            phone_number_match = re.match("[+][8][2]\s+(?P<num>\d+[-]\d+[-]\d+)", phone_number_raw)
            if phone_number_match:
                update_payload['mobile'] = ("0" + phone_number_match.group("num")).replace("-", "")
            else:
                update_payload['mobile'] = phone_number_raw
        # 가입과 동시 로그인
        if result.data['action'] == 'register':
            WishList = Clayful.WishList
            payload = {
                'customer': result.data['customer'],
                'name': 'product_wishlist',
                'description': None
            }
            WishList.create(payload)

            payload = {'token': kakao_access_token}
            result = Customer.authenticate_by_3rd_party('kakao', payload)
            Customer.update(result.data['customer'], update_payload)

        if not is_active(result.data['token']):
            content = {
                'error': {
                    'message': '탈퇴한 회원입니다.'
                }
            }
            return Response(content, status=status.HTTP_409_CONFLICT)

        content = {
            "success": {
                "message": "로그인 완료."
            }
        }
        headers = {
            "Custom-Token": result.data['token']
        }
        return Response(content, headers=headers)
    except Exception as e:
        content = {
            "error": {
                "message": str(e)
            }
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# Naver 소셜 로그인

# 코드 발급
def naver_login(request):
    client_id = getattr(settings, 'NAVER_CLIENT_ID', None)
    local_host = "https://www.byeolshowco.com/"
    # local_host = "http://localhost:8000/"
    redirect_uri = local_host + "user/auth/naver/callback/"
    state = hash(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    request.session['my_state'] = state

    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}")


# 토큰 발급 및 정보 저장
@api_view(['GET'])
def naver_callback(request):
    try:
        client_id = getattr(settings, 'NAVER_CLIENT_ID', None)
        client_secret = getattr(settings, 'NAVER_SECRET_KEY', None)
        code = request.query_params['code']
        state = request.query_params['state']
        my_state = str(request.session['my_state'])

        if state != my_state:
            return Response('No hack, Csrf')

        # 토큰 발급
        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
        token_response = token_request.json()
        naver_access_token = token_response.get('access_token')

        # Clayful에 가입
        @Init_Clayful
        def naver_to_clayful():
            Customer = Clayful.Customer
            payload = {'token': naver_access_token}
            result = Customer.authenticate_by_3rd_party('naver', payload)

            headers = {'Authorization': f'Bearer {naver_access_token}'}
            response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
            user_data = response.json()
            update_payload = {
                'alias': user_data['response']['nickname'],
                'name': {
                    'first': user_data['response']['nickname'],
                    'full': user_data['response']['name']
                },
                'email': user_data['response']['email'],
                'mobile': user_data['response']['mobile'].replace("-", ""),
                'groups': ['ZZ9HGQBGPLTA']
            }
            # 가입과 동시에 로그인
            if result.data['action'] == 'register':
                WishList = Clayful.WishList
                payload = {
                    'customer': result.data['customer'],
                    'name': 'product_wishlist',
                    'description': None
                }
                WishList.create(payload)

                payload = {'token': naver_access_token}
                result = Customer.authenticate_by_3rd_party('naver', payload)
                Customer.update(result.data['customer'], update_payload)
            return result

        result = naver_to_clayful()
        content = f"<h1 style='color:#ffffff'>{result.data['token']}</h1>"
        header = {'Custom-Token': result.data['token']}
        return HttpResponse(content)

    except Exception as e:
        print(e)
        content = {
            'error': {
                'message': '로그인에 실패하였습니다.'
            }
        }
        try:
            print(e.is_clayful)
            print(e.model)
            print(e.method)
            print(e.status)
            print(e.headers)
            print(e.code)
            print(e.message)
            content['error']['detail'] = e.message
        except Exception as er:
            pass

        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def naver_token(request):
    try:
        Customer = Clayful.Customer
        naver_access_token = request.data['naver_access_token']
        payload = {'token': naver_access_token}
        result = Customer.authenticate_by_3rd_party('naver', payload)

        headers = {'Authorization': f'Bearer {naver_access_token}'}
        response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
        user_data = response.json()
        update_payload = {
            'alias': user_data['response']['nickname'],
            'name': {
                'first': user_data['response']['nickname'],
                'full': user_data['response']['name']
            },
            'email': user_data['response']['email'],
            'mobile': user_data['response']['mobile'].replace("-", ""),
            'groups': ['ZZ9HGQBGPLTA']
        }
        # 가입과 동시에 로그인
        if result.data['action'] == 'register':
            WishList = Clayful.WishList
            payload = {
                'customer': result.data['customer'],
                'name': 'product_wishlist',
                'description': None
            }
            WishList.create(payload)

            payload = {'token': naver_access_token}
            result = Customer.authenticate_by_3rd_party('naver', payload)
            Customer.update(result.data['customer'], update_payload)

        if not is_active(result.data['token']):
            content = {
                'error': {
                    'message': '탈퇴한 회원입니다.'
                }
            }
            return Response(content, status=status.HTTP_409_CONFLICT)

        content = {
            "success": {
                "message": "로그인 완료."
            }
        }
        headers = {
            "Custom-Token": result.data['token']
        }
        return Response(content, headers=headers)
    except Exception as e:
        content = {
            "error": {
                "message": str(e)
            }
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# Facebook 소셜 로그인

# 코드 발급
def facebook_login(request):
    client_id = getattr(settings, 'FACEBOOK_CLIENT_ID', None)
    host = "https://www.byeolshowco.com/"
    # host = "http://localhost:8000/"
    redirect_uri = host + "user/auth/facebook/callback/"
    state = hash(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    request.session['my_state'] = state

    return redirect(
        f"https://www.facebook.com/v9.0/dialog/oauth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}")


# 토큰 발급 및 정보 저장
@api_view(['GET'])
def facebook_callback(request):
    try:
        host = "https://www.byeolshowco.com/"
        client_id = getattr(settings, 'FACEBOOK_CLIENT_ID', None)
        client_secret = getattr(settings, 'FACEBOOK_SECRET_KEY', None)
        redirect_uri = host + "user/auth/facebook/callback/"
        code = request.query_params['code']
        state = request.query_params['state']
        my_state = str(request.session['my_state'])

        if state != my_state:
            return Response('No hack, Csrf')

        # 토큰 발급
        token_request = requests.get(
            f"https://graph.facebook.com/v9.0/oauth/access_token?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}")
        token_response = token_request.json()

        facebook_access_token = token_response.get('access_token')

        # Clayful에 가입
        @Init_Clayful
        def facebook_to_clayful():
            Customer = Clayful.Customer
            payload = {'token': facebook_access_token}
            result = Customer.authenticate_by_3rd_party('facebook', payload)
            # 가입과 동시에 로그인
            if result.data['action'] == 'register':
                WishList = Clayful.WishList
                payload = {
                    'customer': result.data['customer'],
                    'name': 'product_wishlist',
                    'description': None
                }
                WishList.create(payload)

                payload = {'token': facebook_access_token}
                result = Customer.authenticate_by_3rd_party('facebook', payload)
                Customer.update(result.data['customer'], {'groups': ['ZZ9HGQBGPLTA']})
            return result

        result = facebook_to_clayful()
        content = f"<h1 style='color:#ffffff'>{result.data['token']}</h1>"
        header = {'Custom-Token': result.data['token']}
        return HttpResponse(content)

    except Exception as e:
        print(e)
        content = {
            'error': {
                'message': '로그인에 실패하였습니다.'
            }
        }
        try:
            print(e.code)
            print(e.message)
            content['error']['detail'] = e.message
        except Exception as er:
            pass
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def facebook_token(request):
    try:
        Customer = Clayful.Customer
        facebook_access_token = request.data['facebook_access_token']
        payload = {'token': facebook_access_token}
        result = Customer.authenticate_by_3rd_party('facebook', payload)
        # 가입과 동시에 로그인
        if result.data['action'] == 'register':
            WishList = Clayful.WishList
            payload = {
                'customer': result.data['customer'],
                'name': 'product_wishlist',
                'description': None
            }
            WishList.create(payload)

            payload = {'token': facebook_access_token}
            result = Customer.authenticate_by_3rd_party('facebook', payload)
            Customer.update(result.data['customer'], {'groups': ['ZZ9HGQBGPLTA']})

        if not is_active(result.data['token']):
            content = {
                'error': {
                    'message': '탈퇴한 회원입니다.'
                }
            }
            return Response(content, status=status.HTTP_409_CONFLICT)

        content = {
            "success": {
                "message": "로그인 완료."
            }
        }
        headers = {
            "Custom-Token": result.data['token']
        }
        return Response(content, headers=headers)
    except Exception as e:
        content = {
            "error": {
                "message": str(e)
            }
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# Influencer 팔로우

class influencer_like(APIView):
    # 팔로잉한 인플루엔서 불러오기
    @require_login
    def get(self, request, result):
        try:
            # 첫번째는 공백, 나머지 원소들 ','로 합친다.
            ids_list = result.data['meta']['Following'][1:]
            ids = ','.join(ids_list)
            if ids != "":
                Customer = Clayful.Customer
                options = {
                    'query': {
                        'ids': ids,
                        'group': 'XU79MY58Q2C4',  # 일반고객은 불러오지 못하게 한다.
                    }
                }
                res = Customer.list(options).data
                # 개인 정보 삭제 및 프론트가 요구한 format으로 전환
                for info in res:
                    info['Follower'] = info['meta']['Follower']['raw']
                    info['description'] = info['meta']['description']
                    info['tag'] = info['meta']['tag']
                    info['thumbnail_url'] = info['meta']['thumbnail_url']
                    if not info['avatar']:
                        pass
                    else:
                        info['avatar'] = info['avatar']['url']
                    del (
                        info['name'], info['address'], info['connect'], info['verified'], info['groups'],
                        info['userId'],
                        info['email'], info['gender'], info['birthdate'], info['mobile'], info['phone'],
                        info['lastLoggedInAt'], info['createdAt'], info['updatedAt'], info['meta'])
            else:
                res = []
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
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer

            # 현재 팔로잉 상태를 확인
            if request.data.get('InfluencerId') in result.data['meta']['Following']:
                # 존재하면
                # 팔로워 수 감소
                Customer.increase_metafield(request.data.get('InfluencerId'), 'Follower', {'value': -1})
                # 알림 설정 삭제하기
                unset_alarm_to_influencer(influencer_id=request.data.get('InfluencerId'), user_id=result.data['_id'])
                # influencer 없으면 알아서 예외 처리됨
                # 팔로잉 취소
                payload = {
                    'value': [
                        request.data.get('InfluencerId')
                    ]
                }
                Customer.pull_from_metafield(result.data['_id'], 'Following', payload)

                contents = {
                    "success": {
                        "message": "팔로잉 취소",
                        "status": "0"
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)

            # 팔로워 수 증가
            Customer.increase_metafield(request.data.get('InfluencerId'), 'Follower', {'value': 1})
            # 알림 설정하기
            set_alarm_to_influencer(influencer_id=request.data.get('InfluencerId'), user_id=result.data['_id'])
            # influencerId 없으면 예외처리 됨
            # 팔로잉
            payload = {
                'value': [
                    request.data.get('InfluencerId')
                ],
                'unique': True
            }
            Customer.push_to_metafield(result.data['_id'], 'Following', payload)

            # 토큰을 저장해야함
            # set_alarm_to_influencer(result.data['_id'], request.data['token'])
            contents = {
                "success": {
                    "message": "팔로잉",
                    "status": "1"
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            try:
                print(e.code)
                print(e.message)
            except Exception as er:
                pass
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)


# VOD 좋아요
class vod_like(APIView):
    @require_login
    def get(self, request, result):
        try:
            my_vod = MediaSerializerforClient(
                MediaStream.objects.filter(vod_id__in=result.data['meta']['my_vod'][1:]).order_by('-started_at')
                , many=True)
            contents = {
                "success": {
                    "my_vod": my_vod.data
                }
            }
            return Response(contents)
        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request, result):
        try:
            now_vod = MediaStream.objects.get(vod_id=request.data['vod_id'])
            Customer = Clayful.Customer

            # 현재 좋아요 상태를 확인
            if request.data.get('vod_id') in result.data['meta']['my_vod']:
                # 좋아요 취소
                now_vod.like_count -= 1
                now_vod.save()
                payload = {
                    'value': [
                        request.data.get('vod_id')
                    ]
                }
                Customer.pull_from_metafield(result.data['_id'], 'my_vod', payload)

                contents = {
                    "success": {
                        "message": "좋아요 취소",
                        "status": "0"
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)
            # 좋아요
            now_vod.like_count += 1
            now_vod.save()

            payload = {
                'value': [
                    request.data.get('vod_id')
                ],
                'unique': True
            }
            Customer.push_to_metafield(result.data['_id'], 'my_vod', payload)

            contents = {
                "success": {
                    "message": "좋아요",
                    "status": "1"
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)
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
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)


class PushAgree(APIView):
    @require_login
    def get(self, request, result):
        try:
            is_push = result.data['meta']['push_agree']
            contents = {
                "success": {
                    "push_agree": is_push
                }
            }
            return Response(contents)
        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request, result):
        try:
            is_push = not result.data['meta']['push_agree']

            Customer = Clayful.Customer
            payload = {
                'meta': {
                    "push_agree": is_push,
                }
            }
            options = {'customer': request.headers.get('Custom-Token')}
            result = Customer.update_me(payload, options)
            headers = result.headers
            data = result.data

            contents = {
                "success": {
                    "push_agree": is_push
                }
            }
            return Response(contents)

        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)


class UploadToken(APIView):
    @require_login
    def post(self, request, result):
        try:
            # DB에 유저의 firebase 토큰 없으면 저장
            firebase_token = request.data["firebase_token"]
            user_id = result.data['_id']
            if not UserToken.objects.filter(user_id=user_id, firebase_token=firebase_token):
                UserToken.objects.create(user_id=user_id, firebase_token=firebase_token)
            contents = {
                "success": {
                    "message": "토큰을 등록했습니다."
                }
            }
            return Response(contents)

        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)


class DeleteToken(APIView):
    @require_login
    def post(self, request, result):
        try:
            # DB에 유저의 firebase 토큰 있으면 삭제
            firebase_token = request.data["firebase_token"]
            user_id = result.data['_id']

            UserToken.objects.filter(user_id=user_id, firebase_token=firebase_token).all().delete()

            contents = {
                "success": {
                    "message": "토큰을 삭제했습니다."
                }
            }
            return Response(contents)

        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)


class RefundBank(APIView):
    @require_login
    def get(self, request, result):
        try:
            res = result.data
            contents = {
                'refund_holder': res['meta'].get('refund_holder', None),
                'refund_bank': res['meta'].get('refund_bank', None),
                'refund_account': res['meta'].get('refund_account', None)
            }
            return Response(contents)
        except Exception as e:
            contents = {
                'error': {
                    'message': '알 수 없는 오류가 발생했습니다.',
                    'detail': str(e)
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer

            payload = {
                'meta': {
                    'refund_holder': request.data['refund_holder'],
                    'refund_bank': request.data['refund_bank'],
                    'refund_account': request.data['refund_account'],
                }
            }
            options = {'customer': request.headers.get('Custom-Token')}

            Customer.update_me(payload, options)

            contents = payload['meta']
            return Response(contents)

        except Exception as e:
            content = {
                'error': {
                    'message': '정보를 모두 입력해 주세요.'
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class LiveAgreeView(APIView):
    @require_login
    def get(self, request, result):
        try:
            live_push_agree = not LiveNotAgree.objects.filter(user_id=result.data['_id']).exists()
            contents = {
                "success": {
                    "live_push_agree": live_push_agree
                }
            }
            return Response(contents)
        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    @require_login
    def post(self, request, result):
        try:
            live_push_set = LiveNotAgree.objects.filter(user_id=result.data['_id'])
            if live_push_set.exists():
                live_push_set.delete()
                live_push_agree = True
            else:
                LiveNotAgree.objects.create(user_id=result.data['_id'])
                live_push_agree = False

            contents = {
                "success": {
                    "live_push_agree": live_push_agree
                }
            }
            return Response(contents)

        except Exception as e:
            print(e)
            contents = {
                "error": {
                    "message": "잘못된 요청입니다."
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)
