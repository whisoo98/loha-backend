from django.db import models

# Create your models here.
## !Complete!
class Categories (models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    category_no = models.IntegerField(verbose_name='분류 번호')
    category_depth = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(4)], verbose_name='분류 Depth')
    parent_category_no = models.IntegerField(verbose_name='부모 분류 번호')
    category_name = models.CharField(max_length=50, verbose_name='분류명')
    display_type = models.CharField(max_length=1, choices=(
        ('A','PC + 모바일'),
        ('P','PC'),
        ('M','모바일'),
        ('F','모두 사용안함')
    ), verbose_name='쇼핑몰 표시설정')
    full_category_name = models.TextField(verbose_name='분류 전체 이름')
    full_category_no = models.IntegerField(verbose_name='분류 전체 번호')
    root_category_no = models.IntegerField(verbose_name='최상위 분류 번호')
    use_main = models.CharField(max_length=1, choices=(
        ('T','표시함'),
        ('F','표시안함')
    ), verbose_name='메인분류 표시상태')
    use_display = models.CharField(max_length=1, choices=(
        ('T','표시함'),
        ('F','표시안함')
    ), verbose_name='표시상태')
    display_order #?
    soldout_product_display = models.CharField(max_length=1, choices=(
        ('B','품절상품 맨 뒤로'),
        ('N','품절상품 상관없음')
    ), verbose_name='품절상품진열')
    sub_category_product_display = models.CharField(max_length=1, choices=(
        ('T','진열함'),
        ('F','진열안함')
    ), verbose_name='하위분류 상품진열')
    hashtag_product_display = models.CharField(max_length=1, choices=(
        ('T','진열함'),
        ('F','진열안함')
    ), verbose_name='쇼핑 큐레이션 해시태그 상품진열')
    hash_tags #?
    product_display_scope #?
    product_display_type = models.CharField(max_length=1, choices=(
        ('A','자동정렬'),
        ('U','사용자 지정'),
        ('M','자동정렬 + 사용자 지정')
    ), verbose_name='상품분류 진열방법')
    product_display_key = models.CharField(max_length=1, choices=(
        ('A','최근 추가된 상품'),
        ('R','최근 등록상품'),
        ('U','최근 수정상품'),
        ('N','상품명 가나다순'),
        ('P','판매가 높은 상품'),
        ('S','판매량 높은 상품'),
        ('C','조회수가 높은 상품'),
        ('L','좋아요수가 높은 상품')
    ), verbose_name='상품분류 진열방법 키')
    product_display_sort = models.CharField(max_length=1, choices=(
        ('D','내림차순'),
        ('A','오름차순')
    ), verbose_name='상품분류 진열방법 순서')
    product_display_period = models.CharField(max_length=3, choices=(
        ('W','전체기간'),
        ('1D','1일'),
        ('3D','3일'),
        ('7D','7일'),
        ('15D','15일'),
        ('1M','1개월'),
        ('3M','3개월'),
        ('6M','6개월')
    ), verbose_name='진열순서에 대한 기간')
    normal_product_display_type = models.CharField(max_length=1, choices=(
        ('A','자동정렬'),
        ('U','사용자 지정'),
        ('M','자동정렬 + 사용자 지정')
    ), verbose_name='상품분류 진열방법')
    normal_product_display_key = models.CharField(max_length=1, choices=(
        ('A','최근 추가된 상품'),
        ('R','최근 등록상품'),
        ('U','최근 수정상품'),
        ('N','상품명 가나다순'),
        ('P','판매가 높은 상품'),
        ('S','판매량 높은 상품'),
        ('C','조회수가 높은 상품'),
        ('L','좋아요수가 높은 상품')
    ), verbose_name='상품분류 진열방법 키')
    normal_product_display_sort = models.CharField(max_length=1, choices=(
        ('D','내림차순'),
        ('A','오름차순')
    ), verbose_name='상품분류 진열방법 순서')
    normal_product_display_period = models.CharField(max_length=3, choices=(
        ('W','전체기간'),
        ('1D','1일'),
        ('3D','3일'),
        ('7D','7일'),
        ('15D','15일'),
        ('1M','1개월'),
        ('3M','3개월'),
        ('6M','6개월')
    ), verbose_name='진열순서에 대한 기간')
    recommend_product_display_type = models.CharField(max_length=1, choices=(
        ('A','자동정렬'),
        ('U','사용자 지정'),
        ('M','자동정렬 + 사용자 지정')
    ), verbose_name='상품분류 진열방법')
    recommend_product_display_key = models.CharField(max_length=1, choices=(
        ('A','최근 추가된 상품'),
        ('R','최근 등록상품'),
        ('U','최근 수정상품'),
        ('N','상품명 가나다순'),
        ('P','판매가 높은 상품'),
        ('S','판매량 높은 상품'),
        ('C','조회수가 높은 상품'),
        ('L','좋아요수가 높은 상품')
    ), verbose_name='상품분류 진열방법 키')
    recommend_product_display_sort = models.CharField(max_length=1, choices=(
        ('D','내림차순'),
        ('A','오름차순')
    ), verbose_name='상품분류 진열방법 순서')
    recommend_product_display_period = models.CharField(max_length=3, choices=(
        ('W','전체기간'),
        ('1D','1일'),
        ('3D','3일'),
        ('7D','7일'),
        ('15D','15일'),
        ('1M','1개월'),
        ('3M','3개월'),
        ('6M','6개월')
    ), verbose_name='진열순서에 대한 기간')
    new_product_display_type = models.CharField(max_length=1, choices=(
        ('A','자동정렬'),
        ('U','사용자 지정'),
        ('M','자동정렬 + 사용자 지정')
    ), verbose_name='상품분류 진열방법')
    new_product_display_key = models.CharField(max_length=1, choices=(
        ('A','최근 추가된 상품'),
        ('R','최근 등록상품'),
        ('U','최근 수정상품'),
        ('N','상품명 가나다순'),
        ('P','판매가 높은 상품'),
        ('S','판매량 높은 상품'),
        ('C','조회수가 높은 상품'),
        ('L','좋아요수가 높은 상품')
    ), verbose_name='상품분류 진열방법 키')
    new_product_display_sort = models.CharField(max_length=1, choices=(
        ('D','내림차순'),
        ('A','오름차순')
    ), verbose_name='상품분류 진열방법 순서')
    new_product_display_period = models.CharField(max_length=3, choices=(
        ('W','전체기간'),
        ('1D','1일'),
        ('3D','3일'),
        ('7D','7일'),
        ('15D','15일'),
        ('1M','1개월'),
        ('3M','3개월'),
        ('6M','6개월')
    ), verbose_name='진열순서에 대한 기간')
    access_authority = models.CharField(max_length=1, choices=(
        ('F','모두 이용 가능'),
        ('T','회원만 이용 가능'),
        ('G','특정회원등급만 이용 가능'),
        ('A','특정 운영자만 이용 가능')
    ), verbose_name='접근권한')

class CategoriesDecorationimages(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    category_no = models.IntegerField(verbose_name='분류 번호')
    use_menu_image_pc = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 PC 메뉴 이미지 사용여부')
    menu_image_pc #? 
    menu_over_image_pc #?
    use_top_image_pc = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 PC 상단 이미지 사용여부')
    top_images_pc #?
    use_title_image_pc = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 PC 타이틀 이미지 사용여부')
    title_image_pc #?
    use_menu_image_mobile = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 모바일 메뉴 이미지 사용여부')
    menu_image_mobile #?
    use_top_image_mobile = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 모바일 상단 이미지 사용여부')
    top_images_mobile #? 
    use_title_image_mobile = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='분류 모바일 타이틀 이미지 사용여부')
    title_image_mobile #?


class CategoriesSeo(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    category_no = models.IntegerField(verbose_name='분류 번호')
    search_engine_exposure = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='검색 엔진 노출 설정')
    meta_title #?
    meta_author #?
    meta_description #?
    meta_keywords #?


class Mains(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    module_code #?
    display_group #?
    group_name = models.TextField(verbose_name='메인분류 명')
    soldout_sort_type = models.CharField(max_length=1, choices=(
        ('B','품절상품 맨 뒤로'),
        ('N','품절상품 상관없음')
    ), verbose_name='품절상품진열')

