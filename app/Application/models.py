from django.db import models

# Create your models here.
## !Complete!
class Apps(models.Model):
    version=models.TextField(default='v2', help_text='Version that using app', verbose_name='버전')
    version_expiration_date=models.DateField(help_text='Date that expired authority of the app', verbose_name='버전 만료일')
    initial_version=models.TextField(help_text='Initial version of the app', verbose_name='최초 버전')
    previous_version=models.TextField(help_text='Previous version of the app', verbose_name='이전 버전')

class AppstoreOrders(models.Model):
    order_id = models.CharField(verbose_name='주문 아이디')
    order_name = models.CharField(verbose_name='주문명')
    order_amoun = models.IntegerField(verbose_name='주문금액')
    currency = models.CharField(choices=(
        ('KRW','원'),
        ('USD','달러'),
        ('JPY','엔')
    ), default='KRW', verbose_name='화폐단위')
    return_url#URL
    automatic_payment = models.CharField(max_length=1, choices=(
        ('T', '사용함'),
        ('F', 사용안함)
    ), verbose_name='정기과금 여부')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='주문 생성일')
    confirmation_url#URL

class AppstorePayments(models.Model):
    order_id = models.CharField(verbose_name='주문 아이디')
    payment_status = models.CharField(choices=(
        ('paid','결제완료'),
        ('refund','환불')
    ), verbose_name='결제상태')
    title = models.CharField(verbose_name='결제명')
    approval_no = models.IntegerField(verbose_name='승인번호')
    payment_gateway_name = models.CharField(verbose_name='결제 PG사 이름')
    payment_method = models.CharField(verbose_name='결제수단')
    payment_amount = models.IntegerField(verbose_name='결제 금액')
    refund_amount = models.IntegerField(verbose_name='환불 금액')
    currency = models.CharField(choices=(
        ('KRW','원'),
        ('USD','달러'),
        ('JPY','엔')
    ), default='KRW', verbose_name='화폐단위')
    locale_code = models.CharField(verbose_name='결제국가')
    automatic_payment = models.CharField(max_length=1, choices=(
        ('T', '사용함'),
        ('F', '사용안함')
    ), verbose_name='정기과금 여부')
    pay_date = models.DateTimeField(verbose_name='결제승인일')
    refund_date = models.DateTimeField(verbose_name='환불승인일')
    expiration_date = models.DateTimeField(verbose_name='만료일')
class ScriptTags(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    script_no = models.IntegerField(verbose_name='script의 고유번호')
    client_id = models.CharField(verbose_name='Client ID')
    src #URL
    display_location#경로
    exclude_path#경로
    skin_no = models.IntegerField(verbose_name='스킨 번호')
    created_date = models.DateTimeField(verbose_name='생성일')
    updated_date = models.DateTimeField(verbose_name='수정일')