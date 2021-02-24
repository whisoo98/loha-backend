from django.db import models

# Create your models here.


class MediaStream(models.Model):
    # from mux
    mux_stream_url = models.URLField(null=True)
    mux_stream_id = models.CharField(max_length=200)
    mux_asset_id = models.CharField(max_length=200, null=True)
    mux_asset_playback_url = models.URLField(null=True)

    # About Media
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    influencer_name = models.CharField(max_length=200)
    influencer_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200) # 대표 상품
    product_id = models.CharField(max_length=200) # 대표 상품 ID
    product_price =models.CharField(max_length=200, default='0원') # 대표 상품 가격
    product_brand = models.CharField(max_length=200, null=True)
    product_list = models.CharField(max_length=500, null=True) # 상품 목록
    thumbnail_url = models.URLField(null=True)

    # About

    # for streaming
    # view -> consumer 에서 관리
    status = models.CharField(max_length=20, default='ready') # ready, live, compelete
    started_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)

    # for VOD
    view_count = models.IntegerField(default=0)


