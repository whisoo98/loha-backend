from django.db import models

# Create your models here.
## !Complete!
class Order(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    carrier_id = models.TextField(verbose_name='배송사 아이디')
    shipping_carrier_code = models.TextField(verbose_name='배송사 코드') #배송사 코드 별첨
    shipping_carrier = models.TextField(verbose_name='배송사 명')
    track_shipment_url#URL
    shipping_type = models.TextField(choices=(
        ('A','국내'),
        ('B','국내/해외'),
        ('C','해외')
    ), verbose_name='국내/해외배송 설정')
    contact = models.TextField(verbose_name='대표 연락처')
    secondary_contact = models.TextField(verbose_name='보조 연락처')
    email = models.EmailField(verbose_name='이메일')
    default_shipping_fee = models.IntegerField(verbose_name='기본 배송비')
    homepage_url#URL
    default_shipping_carrier = models.TextField(choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='기본배송사 여부')
    shipping_fee_setting = models.TextField(choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='배송비 설정 여부')
    shipping_fee_setting_detail #?
    express_exception_setting #?
    links #Link

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_product'
        verbose_name = '상품'
        vebose_name_plural = '상품'
