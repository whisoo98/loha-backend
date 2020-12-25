from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from clayful import Clayful
import json
import requests
import datetime
import urllib

'''
# Clayful 초기화 데코레이터
def init_clayful(original_func):
    def wrapper_function(request, *args, **kwargs):
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjhhNzc5NzY4NTlhOTZlMzI3N2NlZmRmNmU2M2MyMmE5Yzk0MGY3NTA2OTk5MDAwMzU4Y2ZlY2MyYzc0NzJhMTIiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3NDkyMjc4LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJTNFdEVUxROVJLTEQifQ.k1TqaUQgs0hLb2DUygPHFApQKigTJnNIexUPq2Rdl4k',
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })
        return original_func()
    return wrapper_function
'''

# 초기화 데코레이터 + csrf 데코
#@init_clayful
# 회원가입, 탈퇴, 정보 수정, 정보 불러오기
class User(APIView):

    # Clayful 초기화  -> decorator로 변경?
    def __init__(self):
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    # 현재 회원정보 출력
    # 로그인 되어 있는 상태
    # @require_login 데코 추가 예정
    def get(self, request):
        if request.session.get('custom_token'):
            try:
                Customer = Clayful.Customer

                options = {
                    'customer': request.session.get('custom_token')
                }

                result = Customer.get_me(options)

                return Response(result.data)

            except Exception as e:
                # Error case
                self.print_error(request, e)
                return Response("error")


        else:
            return Response('not login yet')

    # 회원가입
    # 로그인이 안 되어 있는 상태
    def put(self, request):
        try:
            Customer = Clayful.Customer

            #body에서 데이터를 적절하게 뽑아온다.
            '''
            payload = {
                "userId": request.data['userId'],
                "email": request.data['email'],
                "password": request.data['password'],
                "name": {
                    'full': request.data['name']['full']
                }
            }
            '''
            #print(request.body)
            payload = json.loads(request.data)

            result = Customer.create_me(payload)

            return Response(result.data)

        except Exception as e:
            # Error case
            self.print_error(request, e)
            return Response("error")


    # 회원 정보 수정
    # 로그인 되어 있는 상태
    # @require_login 데코 추가 예정
    def post(self, request):
        try:
            Customer = Clayful.Customer

            # 기존 비밀번호는 필수, 나머지는 선택
            payload = {
                'password': request.data['old_password'],
                'credentials': {
                    'userId': request.data['new_userId'] if request.data['new_userId'] else None,
                    'email': request.data['new_email'] if request.data['new_email'] else None,
                    'password': request.data['new_password'] if request.data['new_password'] else None
                }
            }

            options = {
                'customer': request.session.get('custom_token')
            }

            response = Customer.update_credentials_for_me(payload, options)

            return Response(response.data)

        except Exception as e:
            # Error case
            self.print_error(request, e)
            return Response("error")


    # 회원 탈퇴
    # 로그인 되어 있는 상태
    # @require_login 데코 추가 예정
    def delete(self, request):
        try:
            Customer = Clayful.Customer

            #세션에서 토큰을 관리하고
            options = {
                'customer': request.session.get('custom_token')
            }

            result = Customer.delete_me(options)

            return Response(result.data)

        except Exception as e:
            # Error case
            self.print_error(request, e)
            return Response("error")

    def print_error(request, e):
        print(request.data)
        print(e.is_clayful)
        print(e.model)
        print(e.method)
        print(e.status)
        print(e.headers)
        print(e.code)
        print(e.message)



# 초기화 데코레이터 + csrf 데코 + 로그인 검사 데코
# 로그인, 로그아웃
class Auth(APIView):
    def __init__(self):
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

    # 로그인 상태 확인
    def get(self, request):
        if request.session.get('custom_token'):
            try:
                Customer = Clayful.Customer

                options = {
                    'customer': request.session.get('custom_token')
                }

                result = Customer.get_me(options)

                return Response(result.data)

            except Exception as e:
                # Error case
                self.print_error(request, e)
                return Response("error")


        else:
            return Response('not login yet')

    # 로그인 함수
    # 로그인 안 되어 있는 상탱
    def post(self, request):
        try:
            Customer = Clayful.Customer

            # body에서 'userId', 'password' 필요
            payload = {
                'userId': request.data['userId'],
                'password': request.data['password']
            }

            response = Customer.authenticate(payload)

            request.session['custom'] = response.data['customer']
            request.session['custom_token'] = response.data['token']
            request.session['expiresIn'] = response.data['expiresIn']

            return Response(response.data)

        except Exception as e:
            self.print_error(request, e)
            return Response("error")


    # 로그아웃 함수
    # 로그인 되어 있는 상태
    # def get(self, request):

    def print_error(request, e):
        print(request.data)
        print(e.is_clayful)
        print(e.model)
        print(e.method)
        print(e.status)
        print(e.headers)
        print(e.code)
        print(e.message)



# kakao 소셜 로그인

# 코드 요청
def kakao_login(request):
    app_rest_api_key = "14465e198e48578e5e4afc11e37f48b6"
    redirect_uri = "http://127.0.0.1:8000/user/auth/social/kakao/login/callback/"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code")

# 토큰 요청 및 정보 처리

def kakao_callback(request):
    try:
        app_rest_api_key = "14465e198e48578e5e4afc11e37f48b6"
        redirect_uri = "http://127.0.0.1:8000/user/auth/social/kakao/login/callback/"
        user_token = request.query_params['code']

        #CSRF 공격을 받기위한 문자열, 나중에 추가?
        #state = datetime.datetime.now().strftime()

        # 토큰 획득
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )

        token_response = token_request.json()
        error = token_response.get("error", None)

        if error is not None:
            # kakao api를 사용하다 오류
            # 추후에
            # 이를 위한 페이지 생성 or index로 이동
            print(token_response)
            return Response('kakao 오류 발생')

        kakao_access_token = token_response.get("access_token")
        #print(kakao_access_token)
        # 토큰을 추후에 메세지 발송을 위해 따로 저장을 해야되나 ?
        # 일단 따로 저장 안 하고 진행



        # 사용자 정보 불러오기
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {kakao_access_token}"},
        )
        kakao_account = profile_request.json()

        try:
            # Clayful에 가입
            Clayful.config({
                'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
                'language': 'ko',
                'currency': 'KRW',
                'time_zone': 'Asia/Seoul',
                'debug_language': 'ko',
            })

            Customer = Clayful.Customer

            try:
                payload = {
                    'token': kakao_access_token
                }

                result = Customer.authenticate_by_3rd_party('kakao', payload)

                if result.data['action'] == 'register':
                    result = Customer.authenticate_by_3rd_party('kakao', payload)

                request.session['custom'] = result.data['customer']
                request.session['custom_token'] = result.data['token']
                request.session['expiresIn'] = result.data['expiresIn']

                return redirect("/user/auth/")

            except Exception as e:

                # Error case
                print("kakao clay")
                print(e.message)
                print(e.code)
                return redirect("/user/auth/")

        except Exception as e:
            print("error clayful")
            print(e)
            return redirect("/user/auth/")

    except Exception as e:
        print("error kakao")
        return redirect("/user/auth/")




# Naver 소셜 로그인

# 코드 발급
def naver_login(request):
    client_id = "JIykLOc5AHOv_NmMGl7w"
    redirect_uri = "http://localhost:8000/user/auth/naver/callback/"
    state = hash(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    request.session['my_state'] = state

    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}")


# 토큰 발급 및 정보 저장

@api_view(['GET'])
def naver_callback(request):
    try :
        client_id = "JIykLOc5AHOv_NmMGl7w"
        client_secret = "hGNs9EzyMC"
        code = request.query_params['code']
        state = request.query_params['state']
        my_state = str(request.session['my_state'])


        if state != my_state:
            return Response('No hack, Csrf')

        # 토큰 발급
        token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
        token_response = token_request.json()
        naver_access_token = token_response.get('access_token')

        # Clayful에 가입
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

        Customer = Clayful.Customer

        payload = {
            'token': naver_access_token
        }

        result = Customer.authenticate_by_3rd_party('naver', payload)

        if result.data['action'] == 'register':
            result = Customer.authenticate_by_3rd_party('naver', payload)

        request.session['custom'] = result.data['customer']
        request.session['custom_token'] = result.data['token']
        request.session['expiresIn'] = result.data['expiresIn']

        return redirect("/user/auth/")

    except Exception as e:
        print(e)
        return Response('error naver token')
