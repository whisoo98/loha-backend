from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from clayful import Clayful
from django.conf import settings
import json
import requests
import datetime

import urllib


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
                print(e.model)
                print(e.method)
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
        return Response(result.data)

    # 회원가입
    def put(self, request):
        try:
            Customer = Clayful.Customer
            if request.data['password'] != request.data['re_password']:
                content = "비밀번호가 일치하지 않습니다."
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            payload = {
                'groups': ['ZZ9HGQBGPLTA'], # 일반고객으로 추가
                'userId': request.data['userId'],
                'alias': request.data.get('alias'),
                'email': request.data['email'],
                'password': request.data['password'],
                'name': {
                    'full': request.data['name']
                },
                'mobile': request.data.get('mobile'),
                'phone': request.data.get('phone'),
                'gender': request.data.get('gender'),
                'birthdate': request.data.get('birthdate'),
            }
            if request.data.get('address') is not None:
                payload['address'] = request.data['address']
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
            # 로그인 정보 수정 (이메일, 비밀번호)
            if request.data.get('old_password') is not None:
                payload = {
                    'password': request.data.get('old_password'),
                    'credentials': {
                        'userId': result.data['userId'],
                        'email': result.data['email'] if request.data.get('email') is None else request.data.get(
                            'email'),
                        'password': request.data.get('old_password') if request.data.get(
                            'new_password') is None else request.data.get('new_password'),
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
                'alias': result.data['alias'] if request.data.get('alias') is None else request.data.get('alias'),
                'name': {
                    'full': result.data['name']['full'] if request.data.get('name') is None else request.data.get('name')
                },
                'mobile': result.data['mobile'] if request.data.get('mobile') is None else request.data.get('mobile'),
                'phone': result.data['phone'] if request.data.get('phone') is None else request.data.get('phone'),
                'gender': result.data['gender'] if request.data.get('gender') is None else request.data.get('gender'),
                'birthdate': result.data['birthdate']['raw'] if request.data.get('birthdate') is None else request.data.get('birthdate'),
                'address': result.data['address'] if request.data.get('address') is None else request.data.get('address'),
            }
            Customer.update_me(payload, options)
        except Exception as e:
            self.print_error(e)
            if 'duplicated' in e.code:
                #content = "이미 가입된 아이디 입니다."
                content = {
                    'error': {
                        'message': e.message,
                        'code': e.code
                    }
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            elif 'password' in e.code:
                #content = "잘못된 비밀번호입니다."  # 로그인 정보 변경시
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
            payload = json.dumps(request.data)
            response = Customer.authenticate(payload)
            # header에 정보 저장
            header = {'Custom-Token': response.data['token']}

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
@api_view(['GET'])
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
            # 가입과 동시 로그인
            if result.data['action'] == 'register':
                result = Customer.authenticate_by_3rd_party('kakao', payload)
                Customer.update(result.data['customer'], {'groups': ['QS8YM3ECBUV4']})
            return result

        result = kakao_to_clayful()
        content = {
            'success': {
                'message': '로그인 완료.'
            }
        }
        header = {'Custom-Token': result.data['token']}
        return Response(content, headers=header)
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
        content = "로그인 실패"
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
            # 가입과 동시에 로그인
            if result.data['action'] == 'register':
                result = Customer.authenticate_by_3rd_party('naver', payload)
                Customer.update(result.data['customer'], {'groups': ['QS8YM3ECBUV4']})
            return result

        result = naver_to_clayful()
        content = "로그인 성공"
        header = {'Custom-Token': result.data['token']}
        return Response(content, headers=header)

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
        content = "로그인 실패"
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


# Influencer 팔로우

class influencer_like(APIView):
    @require_login
    def get(self, request, result):
        try:
            contents = {
                "success":{
                    "Influencer_List": result.data['meta']['Following']
                }
            }
            return Response(contents)
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
            if request.data.get('InfluencerId') in result.data['meta']['Following']:
                # 팔로잉 취소
                result.data['meta']['Following'].remove(request.data.get('InfluencerId'))
                payload = {
                    'meta': {
                        'Following': result.data['meta']['Following']
                    }
                }
                Customer.increase_metafield(result.data['_id'], 'Follower', {'value': -1})
                # influencer 없으면 알아서 예외 처리됨
                Customer.update(result.data['_id'], payload)
                contents = {
                    "success": {
                        "message": "팔로잉 취소",
                        "status": "0"
                    }
                }
                return Response(contents, status=status.HTTP_202_ACCEPTED)
            # 팔로잉
            payload = {
                'meta': {
                    'Following': result.data['meta']['Following'] + [request.data.get('InfluencerId')]
                }
            }
            Customer.increase_metafield(result.data['_id'], 'Follower', {'value': 1})
            # influencer 없으면 알아서 예외 처리됨
            Customer.update(result.data['_id'], payload)
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
