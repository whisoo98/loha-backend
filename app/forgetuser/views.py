# Create your views here.

import random
import string

from clayful import Clayful
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import Response


@api_view(['POST'])
def find_id(request):
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
                'email': request.data.get('email'),
                'fields': 'userId,social'
            }
        }

        result = Customer.list(options)

        # 존재하지 않는 아이디
        if not result.data:
            contents = {
                "error": {
                    "message": '존재하지 않는 이메일입니다.'
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

        # 아이디 존재 && 소셜로그인 아님
        if not result.data[0]['social']:
            contents = {
                "success": {
                    "id": result.data[0]['userId'][:4] + '*' * (len(result.data[0]['userId']) - 4)
                }
            }

            return Response(contents, status=status.HTTP_202_ACCEPTED)

        contents = {
            "error": {
                "message": '소셜로그인 계정입니다.',
                "social": result.data[0]['social'][0]['vendor']
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        content = {
            'error': {
                'message': e
            }
        }

        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_certificate(request):
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
                'userId': request.data.get('userId'),
                'fields': '_id,userId,email,social,name,country'
            }
        }

        result = Customer.list(options)

        # 아이디 존재 x
        if not result.data or result.data[0]['email'] != request.data['email']:
            contents = {
                "error": {
                    "message": '존재하지 않는 아이디/이메일입니다.'
                }
            }
            return Response(contents, status=status.HTTP_400_BAD_REQUEST)

        # 이메일도 동일 할때

        # 인증용 이메일로 전송
        payload = {
            'userId': request.data['userId'],
            'expiresIn': 259200,
            'scope': 'reset-password'
        }
        contents = {
            'customer_id': result.data[0]['_id']
        }
        Customer.request_verification_email(payload, options)
        return Response(contents, status=status.HTTP_202_ACCEPTED)

    except Exception as e:

        # Error case
        print(e)
        # print(e.code)
        contents = {
            "error": {
                "message": str(e)
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)


# 이메일에서 비밀번호 변경시 넘어가는 링크
@api_view(['GET'])
def reset_password(request):
    try:
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })
        Customer = Clayful.Customer

        # 임의의 문자열로 비밀번호 변경
        tmp_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        payload = {
            'secret': request.GET.get('secret', None),
            'password': tmp_password
        }
        result = Customer.reset_password(request.GET.get('customer', None), payload)

        if result.data['reset']:
            contents = {
                "success": {
                    "message": tmp_password
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)

        contents = {
            "error": {
                "message": "알 수 없는 오류."
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        contents = {
            "error": {
                "message": e.message
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)


# 이메일에서 비밀번호 변경시 넘어가는 링크
@api_view(['POST'])
def forgot_change(request):
    try:
        Clayful.config({
            'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })
        Customer = Clayful.Customer

        # 임의의 문자열로 비밀번호 변경
        secret = request.data['secret']
        customer_id = request.data['customer_id']
        change_password = request.data['password']
        payload = {
            'secret': secret,
            'password': change_password
        }
        result = Customer.reset_password(customer_id, payload)

        if result.data['reset']:
            contents = {
                "success": {
                    "message": "비밀번호가 변경되었습니다."
                }
            }
            return Response(contents, status=status.HTTP_202_ACCEPTED)

        contents = {
            "error": {
                "message": "알 수 없는 오류."
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        contents = {
            "error": {
                "message": str(e)
            }
        }
        return Response(contents, status=status.HTTP_400_BAD_REQUEST)
