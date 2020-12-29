from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from clayful import Clayful
import json
import requests
import datetime
import urllib

# 로그인 확인 decorator
def require_login(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            Customer = Clayful.Customer
            # 이름, 별명, 이메일, 그룹 불러오기
            query = {
                'raw': True,
                'fields': "userId,country,name,alias,email,groups,phone"
            }
            options = {
                'customer': request.headers.get('custom_token'),
                'query': query
            }
            kwargs['result'] = Customer.get_me(options)
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
            content = "로그인 후 이용해 주세요."
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        return func(self, request, *args, **kwargs)
    return wrapper

# Clayful 초기화 decorator
def Init_Clayful(func):
    def wrapper(*args, **kwargs):
        # Clayful 초기화
        try:
            Clayful.config({
                'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
                'language': 'ko',
                'currency': 'KRW',
                'time_zone': 'Asia/Seoul',
                'debug_language': 'ko',
            })
        except Exception as e:
            print(e)
            content = "에러"
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        #해당 함수 실행
        ret = func(*args, **kwargs)
        return ret

    return wrapper

# 회원가입, 탈퇴, 정보 수정, 정보 불러오기
class User(APIView):

    # Clayful 초기화
    def __init__(self):
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
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
                'mobile': request.data.get('phone')
            }
            result = Customer.create(payload)
            return Response(result.data)
        except Exception as e:
            self.print_error(e)
            try:
                if 'duplicated' in e.code:
                    content = "이미 가입된 아이디 입니다."
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    content = '잘못된 입력입니다.'
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except Exception as err:
                content = '잘못된 입력입니다.'
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정
    @require_login
    def post(self, request, result):
        try:
            Customer = Clayful.Customer
            options = {'customer': request.headers.get('custom_token')}
            # 로그인 정보 수정 (이메일, 비밀번호)
            if request.data.get('old_password') is not None:
                payload = {
                    'password': request.data.get('old_password'),
                    'credentials': {
                        'userId': result.data['userId'],
                        'email': request.data.get('email'),
                        'password': request.data.get('new_password')
                    }
                }
                Customer.update_credentials_for_me(payload, options)
            else:
                content = '비밀번호 입력 필요'
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            # 개인 정보 수정 (이름, 번호, 별명)
            payload = {
                'alias': request.data.get('alias'),
                'name': {
                    'full': request.data['name']
                },
                'mobile': request.data.get('phone')
            }
            Customer.update_me(payload, options)            
        except Exception as e:
            self.print_error(e)
            if 'duplicated' in e.code:
                content = "이미 가입된 아이디 입니다."
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            elif 'password' in e.code:
                content = "잘못된 비밀번호입니다." # 로그인 정보 변경시
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = '잘못된 입력입니다.'
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        content = '변경 완료'
        return Response(content, status=status.HTTP_202_ACCEPTED)

    # 회원 탈퇴
    @require_login
    def delete(self, request, result):
        try:
            Customer = Clayful.Customer
            options = {'customer': request.headers.get('custom_token')}
            Customer.delete_me(options)
        except Exception as e:
            self.print_error(e)
            content = '탈퇴 오류'
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        content = '탈퇴 완료'
        return Response(content, status=status.HTTP_202_ACCEPTED)

    def print_error(request, e):
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
        
# 네이티브 로그인, 로그아웃 with Clayful
class Auth(APIView):
    def __init__(self):
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
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
            header = {'custom_token': response.data['token']}
            #request.session['custom_token'] = response.data['token']
            content = "로그인 성공"
            return Response(content, headers=header)

        except Exception as e:
            self.print_error(e)
            content = "로그인 실패"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃 함수
    def get(self, request):
        if request.headers.get('kakao_token') is not None:
            token = request.headers.get('kakao_token')
            header = {'Authorization': f'Bearer {token}'}
            requests.get("https://kapi.kakao.com//v1/user/logout", headers=header)

        content = " 로그아웃 성공"
        return Response(content)


    def print_error(request, e):
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

# kakao 소셜 로그인

# 코드 요청
def kakao_login(request):
    app_rest_api_key = "14465e198e48578e5e4afc11e37f48b6"
    local_host = "https://www.byeolshowco.com/"
    local_host = "http://127.0.0.1:8000/"
    redirect_uri = local_host + "user/auth/kakao/callback/"
    state = hash(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    request.session['my_state'] = state
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code&state={state}")

# 토큰 요청 및 정보 처리
@api_view(['GET'])
def kakao_callback(request):
    try:
        app_rest_api_key = "14465e198e48578e5e4afc11e37f48b6"
        local_host = "https://www.byeolshowco.com/"
        local_host = "http://127.0.0.1:8000/"
        redirect_uri = local_host + "user/auth/kakao/callback/"
        user_token = request.query_params['code']
        state = request.query_params['state']
        my_state = str(request.session['my_state'])

        #CSRF 방지
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

        #카카오 토큰, 저장 안함
        kakao_access_token = token_response.get("access_token")

        @Init_Clayful
        def kakao_to_clayful():
            Customer = Clayful.Customer
            payload = { 'token': kakao_access_token }
            result = Customer.authenticate_by_3rd_party('kakao', payload)
            # 가입과 동시 로그인
            if result.data['action'] == 'register':
                result = Customer.authenticate_by_3rd_party('kakao', payload)
                Customer.update(result.data['customer'], {'groups' : ['QS8YM3ECBUV4']})
            return result

        result = kakao_to_clayful()
        content = "로그인 성공"
        header = {'custom_token': result.data['token']}
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
    client_id = "JIykLOc5AHOv_NmMGl7w"
    local_host = "https://www.byeolshowco.com/"
    #local_host = "http://localhost:8000/"
    redirect_uri = local_host + "user/auth/naver/callback/"
    state = hash(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    request.session['my_state'] = state

    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}")


# 토큰 발급 및 정보 저장
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
        header = {'custom_token': result.data['token']}
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
