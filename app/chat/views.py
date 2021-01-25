from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import Response
import json
from clayful import Clayful
from pprint import pprint,PrettyPrinter
import pprint
from .models import *
# Create your views here.

## view는 이용하지 않느다.
def room(request):
    stream_id = request.data['stream_id']

    #pprint.pprint(room_name)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(stream_id)),
        'username': mark_safe(json.dumps(request.user.username))
    })