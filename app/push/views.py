from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError

from user.models import UserToken
from .models import *


# 인플루언서 팔로우할 때 알람 설정
def set_alarm_to_influencer(influencer_id, user_id):
    InfluencerAlarm.objects.create(influencer_id=influencer_id, user_id=user_id)


# 인플루언서 언팔할 때 알람 설정 취소
def unset_alarm_to_influencer(influencer_id, user_id):
    InfluencerAlarm.objects.filter(influencer_id=influencer_id, user_id=user_id).delete()


# 라이브 알람 설정할 때 알람 설정
def set_alarm_to_live(vod_id, user_id):
    LiveAlarm.objects.create(vod_id=vod_id, user_id=user_id)


# 라이브 알람 설정 취소
def unset_alarm_to_live(vod_id, user_id=None):
    if user_id is None:  # 방송이 종료되면 모두 삭제
        LiveAlarm.objects.filter(vod_id=vod_id).delete()
    else:  # 한 사람이 삭제
        LiveAlarm.objects.filter(vod_id=vod_id, user_id=user_id).delete()


# 인플루언서 팔로우에 대한 알람 보내기
def alarm_by_influencer(influencer_id, info):
    try:
        registration_tokens = list(
            InfluencerAlarm.objects.filter(influencer_id=influencer_id).values_list('token', flat=True))
        response = []
        for token in registration_tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    # title='제목입니다.',
                    # body='내용입니다.',
                    # image='https://cdn.clayful.io/stores/45TGXB8XLAKJ.9733A4KD92ZE/images/HR5TCPDCF93D/v1/%EC%97%84%EB%A7%88%EC%86%8C%EC%95%88%EC%8B%AC%EC%9C%A0%EC%95%84%EB%93%B1%EC%8B%AC.png'
                    title='Live 알림!',
                    body='Influencer {}님의 방송이 {}에 시작됩니다!'.format(info['influencer'], info['time']),
                    # image=info['image']
                ),
                tokens=token
            )
            response.append(messaging.send(message))
        print('{0} messages were sent successfully'.format(len(response)))

    except FirebaseError as e:
        print(e.message)

    except Exception as e:
        print("알 수 없는 오류가 발생하였습니다.")


# 라이브 알람 설정에 대한 알람 보내기
def alarm_by_live(id, info):
    try:
        registration_tokens = list(LiveAlarm.objects.filter(id=id).values_list('token', flat=True))
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


def alarm_by_user_id(user_ids, info):
    try:
        registration_tokens = []
        for user_id in user_ids:
            registration_tokens += list(
                UserToken.objects.filter(user_id=user_id).values_list('firebase_token', flat=True))
        for token in set(registration_tokens):
            message = messaging.Message(
                notification=messaging.Notification(
                    title=f'{info["influencer"]}님의 방송이 지금 시작됩니다!',
                    body=info['title'],
                    image=str(info['image'])
                ),
                data={"Live": str(info['vod_id'])},
                token=token,
            )
            try:
                messaging.send(message)
            except Exception:
                continue
    except Exception as e:
        pass
