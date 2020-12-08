from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser

from clayful import Clayful

import requests

# Create your views here.

@api_view(['GET'])
@parser_classes((JSONParser,))
def product_list(request,collection_id='any'):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs'
    })
    try:
        Product = Clayful.Product

        options = {
            'query': {
                'available' : True,
                #'collection' : collection_name,
                'collection': collection_id,
                #'fields' : 'name,notice'
            },
        }

        result = Product.list(options)

        headers = result.headers
        data = result.data

        return Response(data)

    except Exception as e:
        return Response(e.code)



@api_view(['GET'],['POST'])
@parser_classes((JSONParser,))
def product(request,product_id):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs'
    })
    if(request.method=='GET'):
        try:

            Product = Clayful.Product

            options = {
                'query': {
                    'fields' : '_id,name,summary,description,price,discount,shipping,available,brand,thumbnail,collections,options,variants,meta.stream_url'
                },
            }

            result = Product.get(product_id, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)

    elif(request.method=='POST'):
        try:
            Product = Clayful.Product

            payload = {

            }

            options = {

            }

            result = Product.create(product_id,payload, options)

            headers = result.headers
            data = result.data

            return Response(data)

        except Exception as e:
            return Response(e.code)


@api_view(['POST'])
@parser_classes((JSONParser,))
def product_create(reqeust):
    Clayful.config({
        'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc3MGYzMDA2MTlkYjRhMjBiOGYyY2E5MzZlMDU5YzBmMjE4ZTFjNTE2YmI2ZmQzOWQxN2MyZTE0NTIzN2MzMzAiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjAwNjc5ODY3LCJzdG9yZSI6IjQ1VEdYQjhYTEFLSi45NzMzQTRLRDkyWkUiLCJzdWIiOiJSTUM4WldVUTRFWkUifQ.tcG30RcADqDIj73fRbcIi8b2_u3LlhtXWVaL3SawHRs'
    })
    try:
        Product = Clayful.Product

        payload = {

        }

        options = {

        }

        result = Product.create(payload, options)

        headers = result.headers
        data = result.data

        return Response(data)

    except Exception as e:
        return Response(e.code)

