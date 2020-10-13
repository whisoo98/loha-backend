from django.db import models

# Create your models here.
class Product(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티 쇼핑몰 번호')
    product_no = models.IntegerField(verbose_name='상품번호')
    product_code = models.CharField(max_length = 8, verbose_name='상품코드')
    custom_product_code = models.CharField(max_length=40, verbose_name='자체상품 코드')
    product_name = models.CharField(max_length=250, verbose_name='상품명')
    eng_product_name = models.CharField(max_length=250, verbose_name='영문 상품명')
    supply_product_name =models.CharField(max_length=250, verbose_name='공급사 상품명')
    internal_product_name=models.CharField(max_length=50, verbose_name='상품명 (관리용)')
    model_name=models.CharField(max_length=100, verbose_name='모델명')
    price_excluding_tax=models.IntegerField(verbose_name='상품가(제금제외)')
    price=models.IntegerField(verbose_name='상품 판매가')
    retail_price=models.IntegerField(verbose_name='상품 소비자가')
    supply_price=models.IntegerField(verbose_name='상품 공급가')
    display=models.CharField(choice=(
        ('T','진열함'),
        ('F','진열안함')
        ), verbose_name='진열상태')
    selling=models.CharField(choice=(
        ('T','판매함'),
        ('F','판매안함')
        ), verbose_name='판매상태')
    product_condition=models.CharField(choice=(
        ('N','신상품'),
        ('B','반품상품'),
        ('R','재고상품'),
        ('U','중고상품'),
        ('E','전시상품'),
        ('F','리퍼상품'),
        ('S','스크래치상품'),
        ), verbose_name='상품상태')
    product_used_month=models.IntegerField(validators=[MaxValueValidator(2147483647)], verbose_name='중고상품 사용 개월')
    summary_description=models.CharField(max_length=255, verbose_name='상품요약설명')
    product_tag=models.CharField(max_length=200, verbose_name='상품 검색어 - 해시태그')
    margin_rate=models.IntegerField(validators = [MinValueValidator(-999.99),MaxValueValidator(999.99)], verbose_name='마진률')
    tax_type=models.CharField(choice=(
        ('A','과세상품'),
        ('B','면세상품'),
        ('C','영세상품')
        ), verbose_name='과세 구분')
    tax_amount =models.IntegerField(validators = [MinValueValidator(0),MaxValueValidator(100)],verbose_name='과세율')
    price_content= models.CharField(max_length=20, verbose_name='판매가 대체문구 - 품절 or 판매불가')
    buy_limit_by_product=models.CharField(choice=(
        ('T','사용함'),
        ('F','사용안함')
        ), verbose_name='구매제한 개별 설정여부')
    buy_limit_type=models.CharField(choice=(
        ('N','회원만 구매하며 구매버튼 감추기'),
        ('M','회원만 구매하며 구매버튼 보이기'),
        ('F','구매제한 안함')
        ), verbose_name='구매제한')
    repurchase_restriction=models.CharField(choice=(
        ('T','재구매 불가'),
        ('F','제한안함')
        ), verbose_name='재구매제한')
    single_purchase_restriction=models.CharField(choice=(
        ('T','단독구매 불가'),
        ('F','제한안함')
        ), verbose_name='단독구매제한')
    buy_unit_type=models.CharField(choice=(
        ('P','상품 기준'),
        ('O','품목 기준')
        ), verbose_name='구매단위 타입')
    buy_unit=models.IntegerField(verbose_name='구매단위')
    order_quantity_limit_type=models.CharField(choice=(
        ('P','상품 기준'),
        ('O','품목 기준')
        ), verbose_name='주문수량 제한 기준 ')
    minimum_quantity=models.IntegerField(validators=[MinValueValidator(2147483647)], verbose_name='최소주문수량')
    maximum_quantity=models.IntegerField(validators=[MaxValueValidator(2147483647)], verbose_name='최대주문수량')
    points_by_product=models.CharField(choice=(
        ('T','개별설정'),
        ('F','기본설정 사용')
        ), verbose_name='적립금 개별설정 설정 여부')
    points_setting_by_paymen=models.CharField(choice=(
        ('B','기본 적립금설정 사용'),
        ('C','결제방식에 따른 적립')
        ), verbose_name='결제방식별 적립금 설정 여부')
    points_amount=models.IntegerField(verbose_name='적립금 설정 정보')
    except_member_points=models.CharField(choice=(
        ('T','회원등급 추가 적립 제외 설정함'),
        ('F','회원등급 추가 적립 제외 설정안함')
        ), verbose_name='회원등급 추가 적립 제외')
    product_volume=models.IntegerField(verbose_name='상품 부피 정보')
    adult_certification=models.CharField(choice=(
        ('T','사용함'),
        ('F','사용안함')
        ), verbose_name='성인인증')
    detail_image
    list_image
    tiny_image
    small_image
    has_option=models.CharField(choice=(
        ('T','옵션사용함'),
        ('F','옵션사용안함')
        ), verbose_name='옵션 사용여부')
    option_type=models.CharField(choice=(
        ('C','조합 일체선택형'),
        ('S','조합 분리선택형'),
        ('E','상품 연동형'),
        ('F','독립 선택형')
        ), verbose_name='옵션 구성방식')
    use_naverpay==models.CharField(choice=(
        ('T','사용함'),
        ('F','사용안함')
        ), verbose_name='네이버페이 사용여부')
    naverpay_type==models.CharField(choice=(
        ('C','네이버페이 + 쇼핑몰 동시판매 상품'),
        ('O','네이버페이 전용상품')
        ), verbose_name='네이버페이 판매타입')
    manufacturer_code=models.CharField(default = 'M0000000', max_length=8, min_lenght=8, verbose_name='제조사 코드')
    trend_code=(default = 'T0000000', max_length=8, min_lenght=8, verbose_name='트렌드 코드')
    brand_code=(default = 'B0000000', max_length=8, min_lenght=8, verbose_name='브랜드 코드')
    supplier_code =(max_length=8, min_lenght=8, verbose_name='공급사 코드')
    made_date
    release_date
    origin_classification==models.CharField(choice=(
        ('F','국내'),
        ('T','국외'),
        ('E','기타')
        ), verbose_name='원산지 국내/국외/기타')
    origin_place_no
    origin_place_value=models.CharField(max_length= 30,verbose_name='원산지 기타정보 - 기타의 경우 직접 입력')
    made_in_code=models.CharField(verbose_name='원산지국가코드')
    icon_show_period
    icon
    hscode=models.CharField(verbose_name='HS코드')
    product_weight = models.IntegerField(verbose_name='상품 중량(kg)')
    product_material = models.CharField(verbose_name='상품소재')
    created_date
    updated_date
    english_product_material=models.CharField(verbose_name='영문 상품 소재')
    cloth_fabric=models.CharField(choice=(
        ('woven','직물'),
        ('knit','편물')
        ), verbose_name='옷감 - 일본택배사')
    list_icon
    select_one_by_option=models.CharField(choice=(
        ('T','사용함'),
        ('F','사용안함')
        ), verbose_name='옵션별로 한 개씩 선택(독립형 옵션)')
    approve_status==models.CharField(choice=(
        ('N','승인요청 (신규상품)'),
        ('E','승인요청 (상품수정)'),
        ('C','승인완료'),
        ('R','승인거절'),
        ('I','검수진행중'),
        ('Empty Value','요청된적 없음')
        ), verbose_name='승인요청 결과')
    classification_code=models.CharField(default = 'C000000A', min_length = 8, max_length= 8,verbose_name='자체분류 코드')
    sold_out=models.CharField(choice=(
        ('T','품절'),
        ('F','품절아님')
        ), verbose_name='품절여부')
    additional_price =models.IntegerField(verbose_name='판매가 추가금액')
    discountprice
    decorationimages
    benefits
    options
    variants
    clearance_category_eng=models.CharField(verbose_name='해외통관용 상품구분 영문명')
    clearance_category_kor=models.CharField(verbose_name='해외통관용 상품구분 국문명')
    clearance_category_code=models.CharField(min_length=8, max_length=8,verbose_name='해외통관코드')
    additionalimages
    memos
    hits
    seo
    category=models.IntegerField(verbose_name='분류 번호')
    project_no=models.IntegerField(verbose_name='기획전 번호')
    description
    mobile_description
    separated_mobile_description=models.CharField(choice=(
        ('T','직접등록'),
        ('F','상품 상세설명 동일')
        ), verbose_name='모바일 별도 등록')
    additional_image
    payment_info
    shipping_info
    exchange_info
    service_info
    product_tax_type_text
    set_product_type==models.CharField(choice=(
        ('C','일반세트'),
        ('S','분리세트')
        ), verbose_name='세트상품 타입')
    country_hscode=models.CharField(verbose_name='국가별 HS 코드')
    simple_description
    tags
    shipping_fee_by_product=models.CharField(choice=(
        ('T','사용함'),
        ('F','사용안함')
        ), verbose_name='개별배송여부')
    shipping_method	=models.IntegerField(choices=(
        (01, '택배'),
        (02, '빠른등기'),
        (03, '일반등기'),
        (04, '직접배송'),
        (05, '퀵배송'),
        (06, '기타'),
        (07, '화물배송'),
        (08, '매장직접수령'),
        (09, '배송필요없음')
    ), verbose_name='배송방법')
    prepaid_shipping_fee=models.CharField(choice=(
        ('C','착불'),
        ('P','선결제'),
        ('B','선결제/착불')
        ), verbose_name='배송비 선결제 결정')
    shipping_period
    shipping_scope=models.CharField(choice=(
        ('A','국내배송'),
        ('B','해외배송'),
        ('C','국내/해외배송')
        ), verbose_name='배송정보')
    shipping_area=models.CharField(max_length= 255,verbose_name='배송지역')
    shipping_fee_type=models.CharField(choice=(
        ('T','배송비 무료'),
        ('R','고정배송비 사용'),
        ('M','구매 금액에 따른 부과'),
        ('D','구매 금액별 차등 배송료 사용'),
        ('W','상품 무게별 차등 배송료 사용'),
        ('C','상품 수량별 차등 배송료 사용'),
        ('N','상품 수량에 비례하여 배송료 부과')
        ), verbose_name='배송비 타입')
    shipping_rates
    origin_place_code
    additional_information
    image_upload_type=models.CharField(choice=(
        ('A','대표이미지등록'),
        ('B','개별이미지등록'),
        ('C','웹FTP 등록')
        ), verbose_name='이미지 업로드 타입')
    main	
    relational_product



    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_product'
        verbose_name = '상품'
        verbose_name_plural = '상품'
