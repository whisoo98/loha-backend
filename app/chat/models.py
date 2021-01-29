from django.db import models


# Create your models here.

class RoomUser(models.Model):
    room_name = models.ForeignKey('Room', on_delete=models.CASCADE, db_index=False, db_column='room')
    username = models.TextField()

    def __str(self):
        return self.username


class Room(models.Model):
    room_name = models.TextField(primary_key=True)
    room_streamer = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, db_index=False, db_column='room')
    # room = models.TextField()
    author = models.TextField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    def fetch_messages(room_name):
        return Message.objects.filter(room=room_name).order_by('timestamp').all()

    fetch_messages = staticmethod(fetch_messages)