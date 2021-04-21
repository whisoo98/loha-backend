from django.db import models


class UserToken(models.Model):
    user_id = models.CharField(max_length=50)
    firebase_token = models.CharField(max_length=50)





