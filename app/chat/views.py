import json

from django.shortcuts import render
from django.utils.safestring import mark_safe


def index(request):
    return render(request, 'chat/index.html', {})


## view는 이용하지 않느다.
def room(request, room_name):
    stream_id = room_name

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(stream_id)),
        'username': mark_safe(json.dumps(request.user.username))
    })
