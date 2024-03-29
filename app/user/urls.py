"""loha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import *

urlpatterns = [
    path('', User.as_view()),
    path('checkalias/', check_name),
    path('influencer/like/', influencer_like.as_view()),
    path('myvod/', vod_like.as_view()),
    path('auth/', Auth.as_view()),
    path('auth/kakao/login/', kakao_login),
    path('auth/kakao/callback/', kakao_callback),
    path('auth/kakao/token/', kakao_token),
    path('auth/naver/login/', naver_login),
    path('auth/naver/callback/', naver_callback),
    path('auth/naver/token/', naver_token),
    path('auth/facebook/login/', facebook_login),
    path('auth/facebook/callback/', facebook_callback),
    path('auth/facebook/token/', facebook_token),
    path('push_agree/', PushAgree.as_view()),
    path('upload_token/', UploadToken.as_view()),
    path('delete_token/', DeleteToken.as_view()),
    path('refund_bank/', RefundBank.as_view()),
    path('live-agree/', LiveAgreeView.as_view()),
    path('unsubscribe/', Unsubcribe.as_view()),
    path('active/', Active.as_view()),
]
