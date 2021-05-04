from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings

from rest_framework.status import *
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from clayful import Clayful, ClayfulException
import datetime

from media.models import MediaStream
from media.serializers import MediaSerializerforClient


@api_view(['GET'])
def catalog_list(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })
    try:
        Catalog = Clayful.Catalog

        options = {
            'query': {
                'limit': 7
            },
        }

        result = Catalog.list(options)

        headers = result.headers
        data = result.data
        # 별쇼 특별전은 카탈로그에 띄우지 않기

        for catalog in data:
            if catalog['title'] == "별쇼 특별전":
                data.remove(catalog)
            else:
                catalog['createdAt'] = catalog['createdAt']['raw']
                catalog['updatedAt'] = catalog['updatedAt']['raw']
            '''
            if catalog['meta']['DeletedAt'] is not None:
                Due = catalog['meta']['DeletedAt']=catalog['meta']['DeletedAt']['raw']
                Due = datetime.datetime.strptime(Due, '%Y-%m-%dT%H:%M:%S.%fZ')
                if Due <= datetime.datetime.now():
                    Catalog.delete(catalog['_id'],{})
                    '''

        return Response(data, status=HTTP_200_OK)


    except ClayfulException as e:

        return Response(e.code + ' ' + e.message, status=e.status)

    except Exception as e:

        print(e)

        return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)


class Catalog(APIView):
    def get(self, request, catalog_id):
        try:
            Catalog = Clayful.Catalog
            options = {
                'query': {
                    'fields': 'meta.ids'
                }
            }
            result = Catalog.get(catalog_id, options).data
            collection_ids = result['meta']['ids']

            my_vod = []
            for collection_id in collection_ids:
                options = {
                    'query': {
                        'raw': True,
                        'fields': 'meta,name',
                        'collection': collection_id,
                        'limit': 120,
                    }
                }
                Product = Clayful.Product
                result = Product.list(options).data
                related_vod = result[0]['meta']['my_vod'][1:]
                medias = MediaStream.objects.filter(vod_id__in=related_vod, status="completed").order_by('?')
                if len(medias) > 10:
                    medias = medias[:10]
                Collection = Clayful.Collection
                options = {
                    'query': {
                        'fields': 'name'
                    }
                }
                result = Collection.get(collection_id, options).data
                name = result['name']
                vods = MediaSerializerforClient(medias, many=True).data
                my_vod.append({'name': name, 'vods': vods})
            return Response(my_vod)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
