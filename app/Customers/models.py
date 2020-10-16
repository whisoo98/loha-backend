from django.db import models

# Create your models here.
class CustomerGroups(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    group_no = models.IntegerField(verbose_name='회원등급번호')
    group_name = models.TextField()
    group_description = models.CharField(max_length=1, choices=(
        ('',''),
        ('',''),
        ('','')
    ), verbose_name='혜택 결제조건')
    benefits_paymethod = models.CharField(max_length=1, choices=(
        ('A','모든 결제'),
        ('B','현금 결제(무통장)'),
        ('C','현금 결제 외 모든 결제')
    ), verbose_name='혜택 결제조건')
    buy_benefits = models.CharField(max_length=1, choices=(
        ('F','혜택없음'),
        ('D','구매금액 할인'),
        ('M','적립금 지급'),
        ('P','할인/적립 동시적용')
    ), verbose_name='구매시 할인/적립 혜택')
    ship_benefits = models.CharField(max_length=1, choices=(
        ('T','배송비무료설정'),
        ('F','배송비무료설정안함')
    ), verbose_name='배송비 혜택')
    product_availability = models.CharField(max_length=1, choices=(
        ('P','상품별 가격할인만 적용'),
        ('M','회원등급별 가격할인만 적용'),
        ('A','둘다적용')
    ), verbose_name='상품별 할인 중복설정')
    discount_information #?
    points_information #?
    mobile_discount_information #?
    mobile_points_information #?

class CustomerGroupsCustomers(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    group_no = models.IntegerField(verbose_name='회원등급번호')
    member_id = models.TextField(verbose_name='회원아이디')
    fixed_group = models.CharField(max_length=1, choices=(
        ('T','고정함'),
        ('F','고정안함')
    ), verbose_name='회원등급 고정 여부')

class Customers(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    member_id = models.CharField(max_length=20, verbose_name='회원아이디')
    group_no = models.IntegerField(verbose_name='회원등급번호')
    member_authentication = models.CharField(max_length=1, choices=(
        ('T','인증'),
        ('F','미인증'),
        ('B','특별관리회원'),
        ('J','14세미만회원')
    ), verbose_name='회원인증여부')
    use_blacklist = models.CharField(max_length=1, choices=(
        ('T','설정함'),
        ('F','설정안함')
    ), verbose_name='불량회원설정')
    blacklist_type = models.CharField(max_length=1, choices=(
        ('P','상품구매차단'),
        ('L','로그인차단'),
        ('A','로그인&상품구매 차단')
    ), verbose_name='불량회원 차단설정')
    sms = models.CharField(max_length=1, choices=(
        ('T','수신함'),
        ('F','수신안함')
    ), verbose_name='SMS 수신여부')
    news_mail = models.CharField(max_length=1, choices=(
        ('T','수신함'),
        ('F','수신안함')
    ), verbose_name='뉴스메일 수신여부')
    solar_calendar = models.CharField(max_length=1, choices=(
        ('T','양력'),
        ('F','음력')
    ), verbose_name='양력여부')
    total_points = models.IntegerField(verbose_name= '총 적립금')
    available_points = models.IntegerField(verbose_name= '가용 적립금')
    used_points = models.IntegerField(verbose_name= '사용 적립금')
    pointfy_member = models.CharField(max_length=1, choices=(
        ('T','설정함'),
        ('F','설정안함')
    ), verbose_name='통합멤버쉽 회원여부')
    last_login_date = models.DateTimeField(auto_now=True, verbose_name='최근 접속일시')
    gender = models.CharField(max_length=1, choices=(
        ('M','남자'),
        ('F','여자')
    ), verbose_name='성별')
    use_mobile_app = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='모바일앱 사용여부')
    available_credits = models.IntegerField(verbose_name='가용 예치금')
    created_date = models.DateField(auto_now_add=True, verbose_name='가입일')
    fixed_group = models.CharField(max_length=1, choices=(
        ('T','고정함'),
        ('F','고정안함')
    ), verbose_name='회원등급 고정 여부')

class CustomersMeomos(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    memo_no = models.IntegerField(verbose_name='메모 번호')
    author_id = models.TextField(verbose_name='작성자 아이디')
    memo = models.TextField(verbose_name='메모 내용')
    important_flag = models.CharField(max_length=1, choices=(
        ('T','중요 메모'),
        ('F','일반 메모')
    ), verbose_name=중요 메모 여부)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

class CustomersPaymentInformation(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    member_id = models.CharField(max_length=20, verbose_name='회원아이디')
    payment_method = models.TextField(verbose_name='결제수단명')
    payment_gateway = models.TextField(verbose_name='PG 이름')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

        