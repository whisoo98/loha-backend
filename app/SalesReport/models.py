from django.db import models

# Create your models here.
## !Complete!

class ReprotsSalesVolume(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    collection_date = models.DateField(verbose_name='정산 수집 일자')
    collection_hour = models.TimeField(verbose_name='정산 수집 시간')
    product_price = models.IntegerField(verbose_name='상품 판매가')
    product_option_price = models.IntegerField(verbose_name='상품 옵션 가격')
    settle_count = models.IntegerField(verbose_name='결제완료 수량')
    exchane_product_count = models.IntegerField(verbose_name='교환완료 수량')
    cancel_product_count = models.IntegerField(verbose_name='취소완료 수량')
    return_product_count = models.IntegerField(verbose_name='반품완료 수량')
    updated_date = models.TimeField(auto_now_add=True, verbose_name='최종 데이터 갱신 시간')
    variants_code = models.TextField(verbose_name='품목코드')
    product_no = models.IntegerField(verbose_name='상품번호')
    total_sales = models.IntegerField(verbose_name='총 판매 건수')