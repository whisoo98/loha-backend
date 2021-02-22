from django.urls import path, include
from .views import *

urlpatterns = [
    path('reserve/', reserve_live),
    path('start/', start_live),
    path('edit/', edit_my_vod),
    path('delete/', delete_my_vod),
    path('callback/', mux_callback),
    path('alarm/', LiveAlarm.as_view()),
    path('schedule/today/', get_today_schedule),
    path('schedule/future/', get_future_schedule),
]

