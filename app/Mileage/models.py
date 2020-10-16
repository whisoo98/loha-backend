from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
## !Complete!
class Credits(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    member_id = models.CharField(max_length=20, verbose_name='회원아이디')
    group_name = models.TextField(verbose_name='회원등급명')
    increase_amount = models.IntegerField(verbose_name='지급 금액')
    decrease_amount = models.IntegerField(verbose_name='차감 금액')
    balance = models.IntegerField(verbose_name='잔액')
    admin_id = models.TextField(verbose_name='관리자 아이디')
    admin_name = models.TextField(verbose_name='관리자 이름')
    reason = models.TextField(verbose_name='처리사유')
    case#?
    order_id = models.IntegerField(verbose_name='주문번호')

class CreditsReport(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    increase_amount = models.IntegerField(verbose_name='지급 금액')
    decrease_amount = models.IntegerField(verbose_name='차감 금액')
    credits_total = models.IntegerField(verbose_name='예치금 합계')

class Points(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    case#?
    member_id = models.TextField(verbose_name='회원아이디')
    group_name = models.TextField(verbose_name='회원등급명')
    available_points_increase = models.IntegerField(verbose_name='적립금 증가')
    available_points_decrease = models.IntegerField(verbose_name='적립금 차감')
    available_points_total = models.IntegerField(verbose_name='가용 적립금')
    unavailable_points = models.IntegerField(verbose_name='미가용 적립금')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='주문일')
    issue_date = models.DateTimeField(verbose_name='적립금 지급일')
    available_date = models.DateTimeField(verbose_name='미가용 적립금 사용 가능일')
    admin_id = models.TextField(verbose_name='관리자 아이디')
    admin_name = models.TextField(verbose_name='관리자 이름')
    order_id = models.IntegerField(verbose_name='주문번호')
    reason = models.TextField(verbose_name='적립 사유')
    amount = models.IntegerField(default=0,validators=[
            MaxValueValidator(1000000),
            MinValueValidator(1)
        ], verbose_name='적립금 증감액')
    type_ #?

class PointsReport(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    available_points_increase = models.IntegerField(verbose_name='가용 적립금 증가')
    available_points_decrease = models.IntegerField(verbose_name='가용 적립금 차감')
    available_points_total = models.IntegerField(verbose_name='가용 적립금 전체')
    unavailable_points = models.IntegerField(verbose_name='미가용 적립금')
    unavailable_coupon_points = models.IntegerField(verbose_name='미가용 회원 쿠폰 적립금')