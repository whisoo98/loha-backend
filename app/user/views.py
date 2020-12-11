from django.shortcuts import render
from rest_framework.decorators import api_view,parser_classes
from rest_framework.views import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.http.response import  HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from clayful import Clayful
import json

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
            print(request.body)
            payload = json.loads(request.body)

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

