from django.db import models


# Create your models here.

class RoomUser(models.Model):
    room_name = models.ForeignKey('Room', on_delete=models.CASCADE, db_index=False, db_column='room_streamer')
    username = models.CharField(max_length=200)

    def __str(self):
        return self.username

    class Meta:
        unique_together = (('room_name', 'username'),)


class Room(models.Model):
    room_streamer = models.CharField(max_length=200, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_streamer
