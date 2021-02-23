from django.db import models

# Create your models here.


class MediaStream(models.Model):
    # from mux
    stream_url = models.URLField(null=True)
    vod_id = models.CharField(max_length=200, null=True)
    vod_url = models.URLField(null=True)
    stream_id = models.CharField(max_length=200)

    # Clayful info
    title = models.CharField(max_length=200)
    influencer_name = models.CharField(max_length=200)
    influencer_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200) # 대표 상품
    product_id = models.CharField(max_length=200) # 대표 상품 ID
    product_price =models.CharField(max_length=200, default='0원') # 대표 상품 가격
    product_brand = models.CharField(max_length=200, null=True)
    product_list = models.CharField(max_length=500, null=True) # 상품 목록
    description = models.TextField(null=True)
    thumbnail_url = models.URLField(null=True)

    # for streaming
    # view -> consumer 에서 관리
    status = models.CharField(max_length=20, default='ready') # ready, live, compelete
    started_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)

    # for VOD
    view_count = models.IntegerField(default=0)

class MyVod(models.Model):
    user_id = models.CharField(max_length=200)
    vod_id = models.ForeignKey(MediaStream, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

