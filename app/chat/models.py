from django.db import models


# Create your models here.

class RoomUser(models.Model):
    room_name = models.ForeignKey('Room', on_delete=models.CASCADE, db_index=False, db_column='room')
    username = models.TextField()

    def __str(self):
        return self.username


class Room(models.Model):
    room_name = models.CharField(max_length=200)
    room_streamer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name
