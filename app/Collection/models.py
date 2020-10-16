from django.db import models

# Create your models here.
## !Complete!
class Brands(models.Model):
    shop_no = models.IntegerField(default=1, verbose_name='멀티쇼핑몰 번호')
    brand_code #?
    brand_name = models.CharField(max_length=50, verbose_name='브랜드 명')
    use_brand = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='브랜드 사용여부')
    search_keyword = models.CharField(max_length=200, verbose_name='검색어 설정')
    product_count = models.IntegerField(verbose_name='상품수')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

class Classifications(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    classification_code #?
    classification_name = models.CharField(max_length=200, verbose_name='자체분류 명')
    classification_description = models.CharField(max_length=300, verbose_name='자체분류 설명')
    use_classification  = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 사용여부')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    product_count = models.IntegerField(verbose_name='상품수')

class Manufacturers(models.Model):
    shop_noshop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    manufacturer_code #?
    manufacturer_name = models.CharField(max_length=50, verbose_name='제조사명')
    president_name = models.CharField(max_length=30, verbose_name='대표자명')
    use_manufacturer = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='사용여부')
    email = models.EmailField(verbose_name='이메일')
    phone = models.TextField(verbose_name='전화번호')
    homepage #?
    zipcode = models.CharField(max_length=10, verbose_name='우편번호')
    address1 = models.CharField(max_length=255, verbose_name='기본 주소(시/군/구)')
    address2 = models.CharField(max_length=255, verbose_name='상세 주소')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')


class Oringin(models.Model):
    origin_place_no = models.IntegerField(verbose_name='원산지 번호')
    origin_place_name = models.TextField(verbose_name='원산지 이름')
    foreign #?
    made_in_code #?

class Trends(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    trend_code #?
    trend_name = models.CharField(max_length=50, verbose_name='트렌드명')
    use_trend = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='트렌드 사용여부')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    product_count = models.IntegerField(verbose_name='상품수')