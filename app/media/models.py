from django.db import models

# Create your models here.


class MediaStream(models.Model):
    title = models.CharField(max_length=200)
    stream_url = models.URLField(null=True)
    vod_id = models.CharField(max_length=200, null=True)
    vod_url = models.URLField(null=True)
    stream_id = models.CharField(max_length=200)
    product_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=500)
    influencer_name = models.CharField(max_length=200)
    influencer_id = models.CharField(max_length=200)
    description = models.TextField(null=True)
    thumbnail_url = models.URLField(null=True)
    view_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='ready') # ready, live, compelete
    started_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)

class MyVod(models.Model):
    user_id = models.CharField(max_length=200)
    vod_id = models.ForeignKey(MediaStream, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

