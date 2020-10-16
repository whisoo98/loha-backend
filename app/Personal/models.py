from django.db import models

## !Complete!
class Carts(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    basket_product_no = models.IntegerField(verbose_name='장바구니 상품번호')
    member_id = models.TextField(verbose_name='회원아이디')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='담은일자')
    product_no = models.IntegerField(verbose_name='상품번호')
    additional_option_values #?
    variant_code = models.CharField()#?
    quantity = models.IntegerField(verbose_name='수량')
    product_price = models.IntegerField(verbose_name='상품 판매가')
    option_price = models.IntegerField(verbose_name='옵션 추가 가격')
    product_bundle = models.CharField(max_length=1, choices=(
        ('T','세트상품'),
        ('F','세트상품 아님')
    ), verbose_name='세트상품 여부')
    shipping_type = models.CharField(max_length=1, choices=(
        ('A','국내'),
        ('B','해외')
    ), verbose_name='세트상품 여부')
    category_no = models.IntegerField(verbose_name='분류 번호')

class CustomersWishlist(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    wishlist_no = models.IntegerField(verbose_name='관심상품번호')
    product_no = models.IntegerField(verbose_name='상품번호')
    variant_code #?
    additional_option #?
    attached_file_option #?
    price = models.IntegerField(verbose_name='상품 판매가')
    product_bundle = models.CharField(max_length=1, choices=(
        ('T','세트상품'),
        ('F','세트상품 아님')
    ), verbose_name='세트상품 여부')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='담은일자')
    price_content = models.CharField(max_length=20, verbose_name='판매가 대체문구')

class ProductsCarts(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    member_id = models.TextField(verbose_name='회원아이디')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='담은일자')
    product_noproduct_no = models.IntegerField(verbose_name='상품번호')
    variant_code #?
    quantity = models.IntegerField(verbose_name='수량')
    product_bundle = models.CharField(max_length=1, choices=(
        ('T','세트상품'),
        ('F','세트상품 아님')
    ), verbose_name='세트상품 여부')