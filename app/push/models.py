from django.db import models
# Create your models here.

class InfluencerAlarm(models.Model):
    influencer_id = models.CharField(max_length=200, )
    token = models.TextField()

class LiveAlarm(models.Model):
    vod_id = models.CharField(max_length=200)
    token = models.TextField()
