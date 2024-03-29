from clayful import Clayful
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


@api_view(['GET'])
@parser_classes((JSONParser,))
def collection_list(request):
    Clayful.config({
        'client': getattr(settings, 'CLAYFUL_SECRET_KEY', None),
        'language': 'ko',
        'currency': 'KRW',
        'time_zone': 'Asia/Seoul',
        'debug_language': 'ko',
    })

    try:
        Collection = Clayful.Collection

        options = {
            'query': {
                'fields': 'name',
                'limit': 120,
                'page': request.GET.get('page', 1),
                'parent': 'none',  # 최상위 카테고리만 가져옴
            },
        }
        result = Collection.list(options)
        data = result.data

        data[:] = [collection for collection in data if collection['name'] not in ['인플루엔서', '매거진']]

        return Response(data)

    except Exception as e:
        return Response("카테고리를 불러오지 못했습니다.")
