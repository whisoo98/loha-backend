from django.db import models

# Create your models here.
## !Complete!
class Currency(models.Model):
    exchange_rate #?
    standard_currency_code #?
    standard_currency_symbol #?
    shop_currency_code #?
    shop_currency_symbol #?
class Dashboard(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    daily_sales_stats #?
    weekly_sales_stats #?
    monthly_sales_stats #?
    sold_out_products_count = models.IntegerField()
    new_members_count = models.IntegerField()
    board_list #?

class MobbileSetting(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    use_mobile_page = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='모바일 쇼핑몰 사용설정')
    use_mobile_domain_redirection = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='모바일 쇼핑몰 사용설정')

class ProductsSetting(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    calculate_price_based_on = models.CharField(max_length=1, choices=(
        ('S','공급가 대비 마진율'),
        ('A','판매가 대비 마진율'),
        ('P','기본몰 판매가'),
        ('B','상품가')
    ), verbose_name='판매가 계산 기준')
    price_rounding_unit = models.CharField(max_length=2, choices=(
        ('F','절사안함'),
        ('-2','0.01단위'),
        ('-1','0.1단위'),
        ('1','1단위'),
        ('2','10단위'),
        ('0','100단위'),
        ('3','1000단위')
    ), verbose_name='판매가 계산 절사 단위')
    price_rounding_rule = models.CharField(max_length=1, choices=(
        ('L','내림'),
        ('U','올림'),
        ('C','반올림')
    ), verbose_name='판매가 계산 절사 방법')

class Shops(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    default = models.CharField(max_length=1, choices=(
        ('T','기본샵')
        ('F','기본샵 아님'),
    ), verbose_name='기본샵 여부')
    shop_name = models.CharField(max_length=255, verbose_name='쇼핑몰명')
    language_code = models.CharField(max_length=5, choices=(
        ('ko_KR','국문'),
        ('en_US','영문'),
        ('zh_CN','중문(간체)'),
        ('zh_TW','중문(번체)'),
        ('ja_JP','일문'),
        ('vi_VN','베트남어')
    ), verbose_name='언어 코드')
    language_name = models.CharField(max_length=20, verbose_name='기본 언어명')
    currency_code = models.CharField()#?
    currency_name = models.TextField(verbose_name='결제 화폐명')
    reference_currency_code = models.CharField()#?
    reference_currency_name = models.TextField(verbose_name= '참조 화폐명')
    pc_skin_no = models.IntegerField(verbose_name='PC 쇼핑몰 대표 디자인 번호')
    mobile_skin_no = models.IntegerField(verbose_name='PC 쇼핑몰 대표 디자인 번호')
    base_domain #?
    primary_domain #?
    slave_domain #?
    active = models.CharField(max_length=1, choices=(
        ('T','활성화'),
        ('F','비활성화')
    ),verbose_name='활성화 여부')
    timezone #?
    timezone_name #?
    date_format #?
    time_format #?

class SmsSetting(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    use_sms = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='SMS 사용 여부')
    exclude_unsubscriber = models.CharField(max_length=1, choices=(
        ('T','제외'),
        ('F','포함')
    ), verbose_name='수신거부자 제외 발송 여부')
    default_sender = models.TextField(verbose_name='기본 발신번호')
    unsubscribe_phone = models.TextField(verbose_name='무료 수신거부 전화번호')
    send_method = models.CharField(max_length=1, choices=(
        ('S','단문 분할발송'),
        ('L','장문발송(3건 차감)')
    ), verbose_name=' SMS 발송방법')

class Store(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    shop_name = models.TextField(verbose_name='쇼핑몰명')
    mall_id = models.TextField(verbose_name='상점 아이디')
    base_domain #?
    primary_domain #?
    company_registration_no = models.IntegerField(verbose_name='사업자등록번호')
    company_name = models.TextField(verbose_name='상호명')
    president_name = models.TextField(verbose_name='대표자명')
    company_condition = models.TextField(verbose_name='업태')
    company_line = models.TextField(verbose_name='종목')
    country = models.TextField(verbose_name='사업장 국가')
    zipcode = models.TextField(verbose_name='우편번호')
    address1 = models.TextField(verbose_name='기본 주소(시/군/도)')
    address2 = models.TextField(verbose_name='상세 주소')
    phone = models.TextField(verbose_name='전화번호')
    fax = models.TextField(verbose_name='팩스번호')
    email = models.EmailField(verbose_name='이메일')
    mall_url #?
    mail_order_sales_registration = models.CharField(max_length=1, choices=(
        ('T','신고함'),
        ('F','신고안함')
    ), verbose_name='통신 판매업 신고')
    mail_order_sales_registration_number = models.TextField(verbose_name='통신판매신고 번호')
    missing_report_reason_type = models.TextField(verbose_name='통신판매업 미신고 사유')
    missing_report_reason = models.TextField(verbose_name='통신판매업 미신고 사유 상세 내용')
    about_us_contents = models.TextField(verbose_name='회사소개')
    company_map_url #? 
    customer_service_phone = models.TextField(verbose_name='고객센터 상담/주문 전화')
    customer_service_email = models.EmailField(verbose_name='고객센터 상담/주문 이메일')
    customer_service_fax = models.TextField(verbose_name='고객센터 팩스 번호')
    customer_service_sms = models.TextField(verbose_name='고객센터 SMS 수신번호')
    customer_service_hours #?
    privacy_officer_name = models.TextField(verbose_name='개인정보보호 책임자명')
    privacy_officer_position = models.TextField(verbose_name='개인정보보호 책임자 지위')
    privacy_officer_department = models.TextField(verbose_name='개인정보보호 책임자 부서')
    privacy_officer_phone = models.TextField(verbose_name='개인정보보호 책임자 연락처')
    privacy_officer_email = models.EmailField(verbose_name='개인정보보호 책임자 이메일')
    contact_us_mobile = models.CharField(max_length=1, choices=(
        ('T','표시함'),
        ('F','표시안함')
    ), verbose_name='서비스 문의안내 모바일 표시여부')
    contact_us_contents = models.TextField(verbose_name='서비스 문의안내 내용')

class StoreAccounts(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    bank_account_id = models.TextField(verbose_name='무통장 입금 은행 ID')
    bank_name = models.TextField(verbose_name='은행명')
    bank_code = models.CharField(max_length=50, verbose_name='은행코드') #bank_code 별첨
    bank_account_no = models.TextField(verbose_name='계좌번호')
    bank_account_holder = models.TextField(verbose_name='예금주')
    use_account = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='사용여부')

class SubscriptionShipmentsSetting(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    subscription_no = models.TextField(verbose_name='정기배송 상품설정 번호')
    subscription_shipments_name = models.TextField(verbose_name='정기배송 상품설정 명')
    product_binding_type = models.CharField(max_length=1,choices=(
        ('A','전체상품'),
        ('P','개별상품'),
        ('C','상품분류')
    ), verbose_name='정기배송 상품 설정')
    product_list #?
    category_list #?
    use_discount = models.CharField(max_length=1,choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='정기배송 할인 사용여부')
    discount_value_unit = models.CharField(max_length=1, choices=(
        ('P','할인율'),
        ('W','할인 금액')
    ), verbose_name='할인 기준')
    discount_values = models.IntegerField(verbose_name='할인 값')
    related_purchase_quantity = models.CharField(max_length=1,choices=(
        ('T','구매수량에 따라'),
        ('F','구매수량에 관계없이')
    ), verbose_name='구매수량 관계 여부')
    subscription_shipments_cycle_type = models.CharField(max_length=1,choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='배송주기 제공여부')
    subscription_shipments_cycle = models.CharField(max_length=2,choices=(
        ('1W','1주'),
        ('2W','2주'),
        ('3W','3주'),
        ('1M','1개월'),
        ('2M','2개월'),
        ('3M','3개월'),
        ('4M','4개월'),
        ('5M','5개월'),
        ('6M','6개월'),
        ('1Y','1년')
    ), verbose_name='배송주기')
    use_order_price_condition = models.CharField(max_length=1,choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='혜택제공금액기준 사용여부')
    order_price_greater_than = models.IntegerField(verbose_name='혜택제공금액기준 제공 기준금액')
    include_regional_shipping_rate = models.CharField(max_length=1,choices=(
        ('T','포함'),
        ('F','미포함')
    ), verbose_name='지역별배송비 포함여부')

class Users(models.Model):
    user_id = models.TextField(verbose_name='부운영자 아이디')
    user_name = models.TextField(verbose_name='부운영자 명')
    phone = models.TextField(verbose_name='전화번호')
    email = models.EmailField(verbose_name='이메일')
    ip_restriction_type = models.CharField(max_length=1, choices=(
        ('A','사용함'),
        ('F','사용안함')
    ), verbose_name='IP 접근제한')
    admin_type = models.CharField(max_length=1, choices=(
        ('P','대표운영자'),
        ('A','부운영자')
    ), verbose_name='운영자 구분')
    last_login_date = models.DateTimeField(auto_now=True, verbose_name='최근 접속일시')
    shop_no = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='멀티쇼핑몰 번호')
    nick_name = models.TextField(verbose_name='운영자 별명')
    nick_name_icon_type = models.CharField(max_length=1, choices=(
        ('D','직접 아이콘 등록'),
        ('S','샘픔 아이콘 등록')
    ), verbose_name='별명 아이콘 타입')
    nick_name_icon_url #?
    board_exposure_setting #?
    memo = models.TextField(verbose_name='메모')
    available = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='사용여부')
    multishop_access_authority = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='멀티쇼핑몰 접근 권한')
    menu_access_authority #?
    detail_authority_setting #?
    ip_access_restriction #?
    access_permission = models.CharField(max_length=1, choices=(
        ('T','접속 허용시간 설정과 상관없이 항상 관리자 페이지 접속을 허용함'),
        ('F','사용안함')
    ), verbose_name='접속 허용 권한')
