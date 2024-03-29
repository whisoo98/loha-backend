from django.db import models


# Create your models here.


class MediaStream(models.Model):
    # from mux
    mux_livestream_playback_id = models.URLField(null=True)
    mux_livestream_id = models.CharField(max_length=200)
    mux_asset_id = models.CharField(max_length=200, null=True)
    mux_asset_playback_id = models.URLField(null=True)

    # About Media
    vod_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    notice = models.TextField(null=True)
    description = models.TextField(null=True)
    influencer_name = models.CharField(max_length=200)
    influencer_id = models.CharField(max_length=200)
    influencer_thunmbnail = models.URLField(null=True)

    # About product
    product_id = models.CharField(max_length=30, null=True)  # 대표 id
    product_name = models.CharField(max_length=200)  # 대표 상품
    product_price = models.IntegerField(default=0)  # 대표 상품 가격
    product_sale = models.IntegerField(default=0)  # 대표 상품 세일 가격
    product_brand = models.CharField(max_length=200, null=True)  # 대표 상품 brand
    product_thumbnail = models.URLField(null=True)  # 대표상품 섬네일
    product_list = models.CharField(max_length=500, null=True)  # 상품 목록

    # for streaming
    # view -> consumer 에서 관리
    status = models.CharField(max_length=20, default='ready')  # ready, live, compelete
    started_at = models.DateTimeField(null=True)  # 방송 시작
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 날짜
    finished_at = models.DateTimeField(null=True)  # 방송 종료

    # for VOD
    vod_view_count = models.IntegerField(default=0)  # vod 누적 시청 수
    like_count = models.IntegerField(default=0)  # vod 좋아요 수
    push_count = models.IntegerField(default=0)  # live 알람 수

    class Meta:
        unique_together = (('vod_id', 'influencer_id'),)
