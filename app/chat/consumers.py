import json

import websockets
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from media.models import MediaStream
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # check room exist
        try:
            now_room = await self.check_room()
            # add count of vod
            now_room.vod_view_count += 1
            await self.add_count(now_room)
            await self.accept()
        except:
            await self.close()

    # FOR GOING OUT
    async def disconnect(self, close_code):
        try:
            # delete in RoomUser
            await self.delete_user()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'entry_message',
                    'username': 'USEROUT',
                    'id': self.id,
                    'leave': 1,
                    'message': 'USEROUT'
                }
            )

            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except:
            print('error on WS')

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
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
                    'username': "Byeolshow",
                    'count': self.count,
                    'id': self.id,
                    'leave': 0,
                    'message': message
                }
            )
        elif text_data_json['stat'] == 'end':
            message = "방송이 종료되었습니다."

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'live_end',
                    'message': message,
                    'username': "Byeolshow",
                }
            )
        else:
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': self.username,
                    'message': message
                }
            )

    async def entry_message(self, event):
        message = event['message']
        username = event['username']

        # 인원수 증감
        if event['leave'] == 1:
            self.count -= 1
        elif self.id != event['id']:
            self.count += 1

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'stat': 'entry',
            'message': message,
            'count': self.count,
            'username': username,
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

    async def live_end(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'stat': 'end',
            'message': message,
            'username': "Byeolshow",
        }))

    @database_sync_to_async
    def add_count(self, now_room):
        return now_room.save()

    @database_sync_to_async
    def get_count(self):
        return RoomUser.objects.filter(room_name=self.room_name).count()

    @database_sync_to_async
    def check_room(self):
        return MediaStream.objects.get(vod_id=self.room_name, status='live')

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


async def send_end(vod_id):
    async with websockets.connect(f"wss://byeolshowco.com/ws/chat/{vod_id}/") as websocket:
        await websocket.send(
            json.dumps({
                'stat': 'end',
                'message': "방송이 종료되었습니다.",
                'username': "Byeolshow",
            }))
