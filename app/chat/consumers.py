from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
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
        self.username = self.scope['user'].get_username()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.make_new_user()
        await self.accept()

        message = f'{self.username}님이 입장하셨습니다.'
        self.count = await self.get_count()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'entry_message',
                'author': self.username,
                'count': self.count,
                'leave':0,
                'message': message
            }
        )

    # FOR GOING OUT
    async def disconnect(self, close_code):
        # delete in RoomUser
        await self.delete_user()

        message= f'{self.username}님이 나가셨습니다.'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'entry_message',
                'author': self.username,
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
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'author' : self.username,
                'message': message
            }
        )


    async def entry_message(self, event):
        # print(event)
        message = event['message']
        
        # 인원수 증감
        if event['leave'] == 1:
            self.count -= 1
        elif self.username != event['author']:
            self.count += 1


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'stat': 'entry',
            'message': message,
            'count': self.count,
            'author': "Byeolshow",
        }))

    async def chat_message(self, event):
        # print(event)
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'stat': 'chat',
            'message': message,
            'author': author
        }))


    @database_sync_to_async
    def get_count(self):
        return RoomUser.objects.filter(
            room_name=Room.objects.filter(room_name=self.room_name).all()[0]
        ).count()

    @database_sync_to_async
    def make_new_user(self):
        return  RoomUser.objects.create(
            room_name=Room.objects.filter(room_name=self.room_name).all()[0],
            username=self.username
        )

    @database_sync_to_async
    def delete_user(self):
        return RoomUser.objects.filter(
            room_name=Room.objects.filter(room_name=self.room_name).all()[0]
        ).filter(username=self.username).delete()