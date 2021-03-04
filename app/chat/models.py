from django.db import models


# Create your models here.

class RoomUser(models.Model):
    room_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)

    def __str(self):
        return self.username
