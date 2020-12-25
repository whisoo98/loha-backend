from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse,Http404

from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from clayful import Clayful


class CollectionAPI(APIView):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs'
    })

    def get(self, request):
        try:
            Collection = Clayful.Collection
            options = {
                'query' : {
                    'fields' : 'name',
                    'parent' : 'none'
                    #'sort': 'createdAt',
                },
            }
            result = Collection.list(options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

    def post(self, request):
        try:
            Collection = Clayful.Collection
            payload = json.loads(request.body)
            options = {}
            result = Collection.create(payload, options)
            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)

    def put(self, request, collection_id):
        try:
            Collection = Clayful.Collection
            payload = json.loads(request.body)
            options = {}
            result = Collection.update(collection_id, payload, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)

    def delete(self, request, collection_id):
        try:
            Collection = Clayful.Collection
            options = {}
            result = Collection.delete(collection_id, options)
            headers = result.headers
            data = result.data
            return Response(data)

        except Exception as e:
            return Response(e.code)