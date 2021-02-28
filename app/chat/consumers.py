from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
import pprint
from clayful import Clayful
from clayful import ClayfulException
from channels.auth import login
from .models import *
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.accept()

    # FOR GOING OUT
    async def disconnect(self, close_code):
        # delete in RoomUser
        await self.delete_user()

        message= f'{self.username}님이 나가셨습니다.'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'entry_message',
                'username': self.username,
                'leave': 1,
                'message': message
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['stat'] == 'entry':
            self.username = text_data_json['username']

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            self.id = await self.make_new_user()

            message = f'{self.username}님이 입장하셨습니다.'
            self.count = await self.get_count()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'entry_message',
                    'username': self.username,
                    'count': self.count,
                    'leave': 0,
                    'message': message
                }
            )
        else:
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username' : self.username,
                    'message': message
                }
            )


    async def entry_message(self, event):
        # print(event)
        message = event['message']
        
        # 인원수 증감
        if event['leave'] == 1:
            self.count -= 1
        elif self.username != event['username']:
            self.count += 1


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'stat': 'entry',
            'message': message,
            'count': self.count,
            'username': "Byeolshow",
        }))

    async def chat_message(self, event):
        # print(event)
        message = event['message']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'stat': 'chat',
            'message': message,
            'username': username
        }))


    @database_sync_to_async
    def get_count(self):
        return RoomUser.objects.filter(room_name=self.room_name).count()

    @database_sync_to_async
    def make_new_user(self):
        now_user = RoomUser.objects.create(
            room_name=self.room_name,
            username=self.username
        )
        return now_user.id


    @database_sync_to_async
    def delete_user(self):
        return RoomUser.objects.get(pk=self.id).delete()