from django.shortcuts import render

from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from clayful import Clayful
import json

# Create your views here.

@api_view(['GET'])
@parser_classes((JSONParser,))
def usergroup_listAPI(request):
    try:
        Clayful.config({
            'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
        })

        Group = Clayful.Group

        options = {
            'query': {

            },
        }

        result = Group.list(options)

        headers = result.headers
        data = result.data

        return Response(data)

    except Exception as e:

        return Response(e.code)


@api_view(['GET'])
@parser_classes((JSONParser,))
def usergroup_getAPI(request,group_id):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjQ0YmE3ZWI3NTk1MDk3ZmM2ODIwNTEzNDc3YzE5ZGRlZWRmMTgzMjEwYjg1NmJiOGQ2NzRkNWU0M2U5MTg0NTgiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjA3MzQ2NjM2LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJFVTNIQ1g4M1dWNjcifQ.fJkMXfdphEdVA6o4j0wAFl1eOQ5uarJx21AIejrDKlg',
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:

        Group = Clayful.Group

        options = {
            'query': {

            },

        }

        result = Group.get(group_id, options)

        headers = result.headers
        data = result.data

        return Response(data)

    except Exception as e:

        return Response(e.code)
