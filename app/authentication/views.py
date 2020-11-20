from contextlib import redirect_stderr

from django.http import response, request
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.http.response import JsonResponse, HttpResponse
from django.http.request import HttpRequest
from django.views import View
from rest_framework import generics,mixins
from .models import Authentication
import requests
import datetime
import copy

# Create your views here.

    #https://mekind.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id=ehSKOHqFTiAKp4coWMTCaH&state=AAAAAAAA&redirect_uri=https://www.byeolshow.com/oauth/cafe24&scope=mall.read_product

def check( request): #https://{mallid}.cafe24api.com/api/v2/oauth/
    scope = 'mall.read_product'
    auth = Authentication.objects.all().filter(expires_at__gt=datetime.datetime.now()).order_by('-expires_at')
    if(auth.count()==0):
        auth = auth.filter(refresh_token_expires_at__gt=datetime.datetime.now()).order_by('-refresh_token_expires_at')
        if(auth.count()==0): #새로 인증 코드 발급
            redirect('authorize/', scope)
            pass
        else: # refresh 이용
            redirect('token/', auth.first(), 2)
            pass

    else: #정상진행
        redirect('/', auth.first())
        pass

    '''if(row.expired_at == None or datetime.datetime.now()>= row.refresh_token_expires_at): # 새로 인증코드 발급
        state = get_random_string(length=32)
        location = self.get_code(scope=scope, state=state)

        code = location[location.find('code')+5:location.find('&')]
        state_check = location[location.find('state')+6:]

        if(state_check == state): # 새로 토큰 발급
            res = self.get_access_token(code=code)
            row.token = res.headers['acess_token']
            row.expired_at = res.headers['expires_at']
            row.refresh_token = res.headers['refresh_token']
            row.refresh_token_expires_at = res.headers['refresh_token_expires_at']
            row.save()
            pass

        else: # CSRF 오류 -> how?
            pass

    elif (datetime.datetime.now() >= row.expired_at): #Refresh
        res = self.get_access_token_with_refresh(refresh_token=row.refresh_token)
        row.token = res.headers['acess_token']
        row.expired_at = res.headers['expires_at']
        row.refresh_token = res.headers['refresh_token']
        row.refresh_token_expires_at = res.headers['refresh_token_expires_at']
        row.save()
        pass

    else : #정상 진행
        pass'''


def get_code(request): #https://{mallid}.cafe24api.com/api/v2/oauth/authorize
    scope = 'mall.read_product'
    if(request.method=='POST'):
        client_id = 'ehSKOHqFTiAKp4coWMTCaH'
        state = get_random_string(length=32)
        redirect_uri = 'https://www.byeolshow.com/oauth/cafe24'

        url = 'https://mekind.cafe24api.com/api/v2/oauth/authorize?response_type=code'
        url +='&client_id=' + client_id
        url +='&state=' + state
        url +='&redirect_uri=' + redirect_uri
        url +='&scope=' + scope

        response = requests.get(url)
        location = response.headers['location']
        code = location['code']
        state_check = location['state']
        if(state==state_check): #진행
             return redirect('/token/', code)
        else: #진행 X
            pass
    else:
        pass

def get_access_code(request, code): #https://{mallid}.cafe24api.com/api/v2/oauth/token
    if(request.method=='POST'):
        url = "https://mekind.cafe24api.com/api/v2/oauth/token"
        redirect_uri = 'https://www.byeolshow.com/oauth/cafe24'
        #payload = '''grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}'''
        payload = 'grant_type=authorization_code'
        payload +='&code=' + code
        payload +='&redirect_uri=' + redirect_uri

        headers = {
            'Authorization': "Basic "+'ehSKOHqFTiAKp4coWMTCaH'+':'+'T7fVHR5KEaOfu6IKXhszFM',
            'Content-Type': "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        auth = Authentication.objects.all().order_by('expires_at','refresh_token_expires_at').first()
        auth = Authentication(
            client_id=response.headers['client_id'],
            access_token=response.headers['access_token'],
            expires_at=response.headers['expires_at'],
            refresh_token=response.headers['refresh_token'],
            refresh_token_expires_at=response.headers['refresh_token_expires_at'],
        )
        #scopes = response.headers['scopes']
        scopes = 'mall.read_product'
        return redirect(redirect_uri, scopes)
    else:
        pass

def get_access_code_with_refresh(request, refresh_token,flag=2): #https://{mallid}.cafe24api.com/api/v2/oauth/token
    if (request.method == 'POST'):
        url = "https://mekind.cafe24api.com/api/v2/oauth/token"
        # payload = '''grant_type=authorization_code&code={code}&redirect_uri={redirect_uri}'''
        payload = 'grant_type=refresh_token'
        payload += '&refresh_token=' + refresh_token
        redirect_uri ='https://www.byeolshow.com/oauth/cafe24'
        headers = {
            'Authorization': "Basic " + 'ehSKOHqFTiAKp4coWMTCaH'+':'+'T7fVHR5KEaOfu6IKXhszFM',
            'Content-Type': "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        auth = Authentication.objects.get(refresh_token=refresh_token)
        auth = Authentication(
            client_id=response.headers['client_id'],
            access_token=response.headers['access_token'],
            expires_at=response.headers['expires_at'],
            refresh_token=response.headers['refresh_token'],
            refresh_token_expires_at=response.headers['refresh_token_expires_at'],
        )
        #scopes = response.headers['scopes']
        scopes = 'mall.read_product'
        return redirect(redirect_uri, scopes)
    else:
        pass

