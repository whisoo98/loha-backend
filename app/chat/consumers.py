from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import pprint
from clayful import Clayful
from clayful import ClayfulException
from channels.auth import login
from .models import *
from channels.db import database_sync_to_async


class ChatConsumer(WebsocketConsumer):
    # FOR COMMING
    def count_user(self, data):
        room_name = data['room_name']
        count = RoomUser.objects.filter(room_name=room_name).count()
        self.count = count
        content = {
            'command': 'countUser',
            'count': str(count)
        }
        self.send_message(content)

    def connect(self):
        self.username = self.scope['user'].get_username()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # room, is_roomed = Room.objects.get_or_create(room_name=room_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        RoomUser.objects.create(room_name=self.room_name, username=self.username)
        self.accept()

    # FOR GOING OUT
    def disconnect(self, close_code):
        # Leave room group
        RoomUser.objects.filter(room_name=self.room_name).filter(username=self.username).delete()
        # RoomUser.objects.filter(room_name=room_name).filter(username=username).delete()
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def fetch_message(self, data):  ## to replay
        messages = Message.fetch_messages(data['room_name'])
        content = {
            'command': 'fetch_messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['author']
        room = Room.objects.filter(room_name=self.room_name).all()[0]
        message = Message.objects.create(
            room=room,
            author=author,
            content=data['message'])

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_message': fetch_message,
        'new_message': new_message,
        'countUser': count_user
    }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    # for new message method
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

