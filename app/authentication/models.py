from turtle import mode

from django.db import models

# Create your models here.

class Authentication(models.Model):
    objects = models.Manager()
    url = models.URLField(null=True)
    client_id = models.TextField(default='ehSKOHqFTiAKp4coWMTCaH')
    client_secret = models.TextField(default='T7fVHR5KEaOfu6IKXhszFM')
    access_token = models.TextField(null=True)
    expires_at = models.DateTimeField(null=True)
    refresh_token = models.TextField(null=True)
    refresh_token_expires_at = models.DateTimeField(null=True)
    redirect_url = models.URLField(null=True)

    def __str__(self):
        return self.client_id








