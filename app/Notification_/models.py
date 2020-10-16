from django.db import models

# Create your models here.
## !Complete!
class CustomersInviation(models.Model):
    shop_no = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='멀티쇼핑몰 번호')
    member_id = models.CharField(max_length=16, verbose_name='회원아이디')

class Sms(models.Model):
    queue_code #?

class SmsSenders(models.Model):
    sender_no = models.TextField(verbose_name='발신자 아이디')
    sender = models.TextField(verbose_name='발신자 번호')
    auth_status = models.CharField(max_length=2, choices=(
        ('00','삭제'),
        ('10','등록'),
        ('20','심사중'),
        ('30','인증완료'),
        ('40','반려')
    ), verbose_name='인증상태')