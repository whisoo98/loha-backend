from django.urls import path

from .views import *

urlpatterns = [
    path('reserve/', reserve_live),
    path('start/', start_live),
    path('end/', end_vod),
    path('edit/', edit_my_vod),
    path('delete/', delete_my_vod),
    path('callback/', mux_callback),
    path('alarm/', Alarm.as_view()),
    path('schedule/today/ready', get_today_ready_schedule),
    path('schedule/today/live', get_today_live_schedule),
    path('schedule/future/', get_future_schedule),
    path('schedule/ready/', get_ready_schedule),
    path('get/', get_live),
    path('hot/', get_hot_live),
    path('related/', get_related),
    path('live_alarm/', live_alarm),
]
