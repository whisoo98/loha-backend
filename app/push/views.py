import firebase_admin
from firebase_admin import credentials,firestore,messaging,datetime
from firebase_admin.exceptions import FirebaseError
from .models import *
from django.http import HttpResponse
from rest_framework.status import *
from rest_framework.request import Request
from rest_framework.views import APIView
import clayful


# Create your views here.
#TODO:라이브 예약에 대한 구현
#TODO:알람 푸시에 대한 구현

#인플루언서 팔로우할 때 알람 설정
def set_alarm_to_influencer(influencer_id, token):
    InfluencerAlarm.objects.create(influencer_id=influencer_id, token=token)

#인플루언서 언팔할 때 알람 설정 취소
def set_alarm_to_influencer(influencer_id, token):
    InfluencerAlarm.objects.filter(influencer_id=influencer_id, token=token).all().delete()

#라이브 알람 설정할 때 알람 설정
def set_alarm_to_live(Live_id, token):
    LiveAlarm.objects.create(Live_id=Live_id, token=token)

#라이브 알람 설정 취소
def unset_alarm_to_live(Live_id, token=None):
    if token is None: #방송이 종료되면 모두 삭제
        LiveAlarm.objects.fileter(Live_id=Live_id).all().delete()
    else: #한 사람이 삭제
        LiveAlarm.objects.filter(Live_id=Live_id, token=token).all().delete()

#인플루언서 팔로우에 대한 알람 보내기
def alarm_by_influencer(influencer_id, info):

    try:
        registration_tokens = list(InfluencerAlarm.objects.filter(influencer_id=influencer_id).values_list('token',flat=True))
        response = []
        for token in registration_tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    #title='제목입니다.',
                    #body='내용입니다.',
                    #image='https://cdn.clayful.io/stores/45TGXB8XLAKJ.9733A4KD92ZE/images/HR5TCPDCF93D/v1/%EC%97%84%EB%A7%88%EC%86%8C%EC%95%88%EC%8B%AC%EC%9C%A0%EC%95%84%EB%93%B1%EC%8B%AC.png'
                    title='Live 알림!',
                    body='Influencer {}님의 방송이 {}에 시작됩니다!'.format(info['influencer'], info['time']),
                    #image=info['image']
                ),
                tokens=token
            )
            response.append(messaging.send(message))
        print('{0} messages were sent successfully'.format(len(response)))

    except FirebaseError as e:
        print(e.message)

    except Exception as e:
        print("알 수 없는 오류가 발생하였습니다.")

#라이브 알람 설정에 대한 알람 보내기
def alarm_by_live(id, info):
    try:
        registration_tokens = list(LiveAlarm.objects.filter(id=id).values_list('token',flat=True))
        response = []
        for token in registration_tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    # title='제목입니다.',
                    # body='내용입니다.',
                    title='Live 알림!',
                    body='Influencer {}님의 방송이 {}에 시작됩니다!'.format(info['influencer'], info['time']),
                    image='https://cdn.clayful.io/stores/45TGXB8XLAKJ.9733A4KD92ZE/images/HR5TCPDCF93D/v1/%EC%97%84%EB%A7%88%EC%86%8C%EC%95%88%EC%8B%AC%EC%9C%A0%EC%95%84%EB%93%B1%EC%8B%AC.png'
                ),
                tokens=token
            )
            response.append(messaging.send(message))
        print('{0} messages were sent successfully'.format(len(response)))

    except FirebaseError as e:
        print(e.message)

    except Exception as e:
        print("알 수 없는 오류가 발생하였습니다.")