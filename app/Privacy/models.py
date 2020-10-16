from django.db import models

# Create your models here.
class CustomersPrivacy(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    member_id = models.CharField(max_length=20, verbose_name='회원아이디')
    name = models.TextField(verbose_name='이름')
    name_english = models.TextField(verbose_name='영문이름')
    name_phonetic = models.TextField(verbose_name='발음표기 이름 (일본어)')
    phone = models.TextField(verbose_name='전화번호')
    cellphone = models.TextField(verbose_name='휴대전화')
    email = models.EmailField(verbose_name='이메일')
    sms = models.CharField(max_length=1, choices=(
        ('T','수신'),
        ('F','수신안함')
    ), verbose_name='SMS 수신여부')
    news_mail = models.CharField(max_length=1, choices=(
        ('T','수신'),
        ('F','수신안함')
    ), verbose_name='뉴스메일 수신여부')
    wedding_anniversary = models.DateField(verbose_name='결혼기념일')
    birthday = models.DateField(verbose_name='생일')
    solar_calendar = models.CharField(max_length=1, choices=(
        ('T','수신'),
        ('F','수신안함')
    ), verbose_name='양력여부')
    total_points = models.IntegerField(verbose_name='총 적립금')
    available_points = models.IntegerField(verbose_name='가용 적립금')
    used_points = models.IntegerField(verbose_name='사용 적립금')
    city = models.CharField(max_length=255, verbose_name='시/군/도시')
    state = models.CharField(max_length=255, verbose_name='주/도')
    address1 = models.CharField(max_length=255, verbose_name='기본 주소')
    address2 = models.CharField(max_length=255, verbose_name='상세 주소')
    group_no = models.IntegerField(verbose_name='회원등급번호')
    job_class = models.TextField(verbose_name='직종')
    job = models.TextField(verbose_name='직업')
    zipcode = models.CharField(max_length=14, verbose_name='우편번호')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
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
    pointfy_member = models.CharField(max_length=1, choices=(
        ('T','설정함'),
        ('F','설정안함')
    ), verbose_name='통합멤버쉽 회원여부')
    blacklist_type = models.CharField(max_length=1, choices=(
        ('P','상품구매차단'),
        ('L','로그인차단'),
        ('A','로그인&상품구매 차단')
    ), verbose_name='불량회원 차단설정')
    last_login_date = models.DateTimeField(auto_now=True, verbose_name='최근 접속일시')
    member_authority = models.CharField(max_length=1, choices=(
        ('C','일반회원'),
        ('P','대표 운영자'),
        ('A','부운영자'),
        ('S','공급사')
    ), verbose_name='회원권한구분')
    nick_name = models.CharField(max_length=50, verbose_name='운영자 별명')
    recommend_id = models.TextField(verbose_name='추천인 아이디')
    residence = models.TextField(verbose_name='지역코드')
    interest = models.TextField(verbose_name='관심분야')
    gender = models.CharField(max_length=1, choices=(
        ('M','남자'),
        ('F','여자')
    ), verbose_name='성별')
    member_type = models.CharField(max_length=1, choices=(
        ('p','개인'),
        ('c','사업자'),
        ('f','외국인')
    ), verbose_name='회원타입')
    company_type = models.CharField(max_length=1, choices=(
        ('p','개인사업자'),
        ('c','법인사업자')
    ), verbose_name='사업자구분')
    foreigner_type = models.CharField(max_length=1, choices=(
        ('f','외국인등록번호'),
        ('p','여권번호'),
        ('d','국제운전면허증')
    ), verbose_name='외국인 인증방법')
    lifetime_member = models.CharField(max_length=1, choices=(
        ('T','동의함'),
        ('F','동의안함'),
    ), verbose_name='평생회원 동의여부')
    corporate_name = models.TextField(verbose_name='법인명')
    nationality = models.TextField(verbose_name='국적')
    shop_name = models.TextField(verbose_name='쇼핑몰명')
    country_code = models.TextField(verbose_name='국가코드')
    use_mobile_app = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함'),
    ), verbose_name='모바일앱 사용여부')
    join_path = models.CharField(max_length=1, choices=(
        ('P','PC'),
        ('M','모바일'),
    ), verbose_name='가입경로')
    fixed_group = models.CharField(max_length=1, choices=(
        ('T','고정함'),
        ('F','고정안함'),
    ), verbose_name='회원등급 고정 여부')
    available_credits = models.IntegerField(verbose_name='가용 예치금')
    additional_information #?

class ProductsWishlistCustomers(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    member_id = models.TextField(verbose_name='회원아이디
    ')