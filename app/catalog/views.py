from clayful import Clayful, ClayfulException
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

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
                'limit': 120
            },
        }
        result = Catalog.list(options)
        data = result.data
        data[:] = [catalog for catalog in data if catalog['meta']['Type'] not in ['special', 'magazine']]
        # 별쇼 특별전과 매거진 카탈로그에 띄우지 않기
        for catalog in data:
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
        return Response("알 수 없는 예외가 발생했습니다.", status=HTTP_400_BAD_REQUEST)


class Special(APIView):
    def get(self, request):
        try:
            Catalog = Clayful.Catalog
            options = {
                'query': {
                    'limit': 7
                },
            }

            result = Catalog.list(options)
            data = result.data

            special_catalog = [catalog for catalog in data if catalog['meta']['Type'] == "special"]

            collection_ids = special_catalog[0]['meta']['ids']

            options = {
                'query': {
                    'raw': True,
                    'fields': 'meta,name',
                    'collection': ",".join(collection_ids),
                    'limit': 120,
                }
            }
            Product = Clayful.Product
            result = Product.list(options).data
            related_vods = []
            for info in result:
                related_vods += info['meta']['my_vod'][1:]
            medias = MediaStream.objects.filter(vod_id__in=related_vods, status="completed").order_by('?')
            if len(medias) > 5:
                medias = medias[:5]
            my_vod = {'title': special_catalog[0]['title'], 'vods': MediaSerializerforClient(medias, many=True).data}
            return Response(my_vod)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class Magazine(APIView):
    def get(self, request):
        try:
            Catalog = Clayful.Catalog
            options = {
                'query': {
                    'limit': 7
                },
            }

            result = Catalog.list(options)
            data = result.data

            magazines = [catalog for catalog in data if catalog['meta']['Type'] == "magazine"]
            if not magazines:
                return Response([])

            magazine_responses = []
            for magazine in magazines:
                collection_ids = magazine['meta']['ids']

                title = magazine['title']
                description = magazine['description']
                items = magazine['items']
                sub_description = magazine['meta']['sub_description']

                contents = {
                    "title": title,
                    "description": description,
                    "items": items,
                    "sub_description": sub_description,
                    "collection_ids": collection_ids
                }
                magazine_responses.append(contents)

            return Response(magazine_responses)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
