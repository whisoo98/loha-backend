from django.db import models

# Create your models here.
## !Complete!
class Suppliers(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    supplier_code #?
    supplier_name = models.CharField(max_length=100, verbose_name='공급사명')
    status = models.CharField(max_length=1, choices=(
        ('A','거래중'),
        ('P','거래중지'),
        ('N','거래해지')
    ), verbose_name='상태')
    commission = models.IntegerField(verbose_name='수수료')
    payment_period = models.CharField(max_length=1, choices=(
        ('0','선택안함'),
        ('C','일일정산'),
        ('B','주간정산'),
        ('A','월간정산')
    ), verbose_name='정산주기')
    business_item = models.CharField(max_length=255, verbose_name='거래상품 유형')
    payment_type = models.CharField(max_length=1, choices=(
        ('P','수수료형'),
        ('D','매입형')
    ), verbose_name='정산유형')
    supplier_type = models.CharField(max_length=2, choices=(
        ('WS','도매업체'),
        ('SF','사입업체'),
        ('BS','입점업체'),
        ('ET','기타')
    ), verbose_name='공급사구조')
    use_supplier = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='사용여부')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='수정일')
    country_code = models.CharField(max_length=3, choices=(
        ('KOR','한국'),
        ('JPN','일본'),
        ('CHN','중국'),
        ('TWN','대만'),
        ('ETC','기타')
    ), verbose_name='사업장 주소 국가 코드')
    zipcode = models.CharField(max_length=10, verbose_name='우편번호')
    address1 = models.CharField(max_length=255, verbose_name='기본 주소(시/군/구)')
    address2 = models.CharField(max_length=255, verbose_name='상세 주소')
    manager_information #?
    trading_type = models.CharField(max_length=1, choices=(
        ('D','사입'),
        ('C','직배송')
    ), verbose_name='공급사유형')
    payment_method = models.IntegerField(choices=(
        (10,'결제완료'),
        (30,'배송시작'),
        (40,'배송완료')
    ), verbose_name='정산시기')
    payment_start_day = models.IntegerField(choices=(
        (0,'일요일마다 정산 진행'),
        (1,'월요일마다 정산 진행'),
        (2,'화요일마다 정산 진행'),
        (3,'수요일마다 정산 진행'),
        (4,'목요일마다 정산 진행'),
        (5,'금요일마다 정산 진행'),
        (6,'토요일마다 정산 진행')
    ), verbose_name='정산시작 요일')
    payment_end_day = models.IntegerField(choices=(
        (0,'일요일마다 정산 진행'),
        (1,'월요일마다 정산 진행'),
        (2,'화요일마다 정산 진행'),
        (3,'수요일마다 정산 진행'),
        (4,'목요일마다 정산 진행'),
        (5,'금요일마다 정산 진행'),
        (6,'토요일마다 정산 진행')
    ), verbose_name='정산종료 요일')
    payment_start_date = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(31)], verbose_name='정산시작 일')
    payment_end_date = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(31)], verbose_name='정산종료 일')
    bank_code #?
    bank_account_no = models.TextField(verbose_name='계좌번호')
    bank_account_name = models.TextField(verbose_name='예금주')
    phone = models.CharField(max_length=20, verbose_name='전화번호')
    fax = models.CharField(max_length=20, verbose_name='팩스번호')
    market_country_code = models.CharField(max_length=3, choices=(
        ('KOR','한국'),
        ('JPN','일본'),
        ('CHN','중국'),
        ('TWN','대만'),
        ('ETC','기타')
    ), verbose_name='시장 주소 국가 코드')
    market_zipcode = models.CharField(max_length=10, verbose_name='시장주소 우편번호')
    market_address1 = models.CharField(max_length=255, verbose_name='시장 기본 주소')
    market_address2 = models.CharField(max_length=255, verbose_name='시장 상세 주소')
    exchange_country_code = models.CharField(max_length=3, choices=(
        ('KOR','한국'),
        ('JPN','일본'),
        ('CHN','중국'),
        ('TWN','대만'),
        ('ETC','기타')
    ), verbose_name='반품 주소 국가 코드')
    exchange_zipcode = models.CharField(max_length=10, verbose_name='반품주소 우편번호')
    exchange_address1 = models.CharField(max_length=255, verbose_name='반품 기본 주소')
    exchange_address2 = models.CharField(max_length=255, verbose_name='반품 상세 주소')
    homepage_url #?
    mall_url #?
    account_start_date #?
    account_stop_date #?
    show_supplier_info = models.CharField(max_length=100, choices=(
        ('SP','전화번호'),
        ('SM','사업장주소'),
        ('MA','시장주소'),
        ('EA','반품주소'),
        ('MN','담당자명'),
        ('MI','담당자연락처')
    ), verbose_name='사용여부')
    memo = models.CharField(max_length=255, verbose_name='메모')
    company_registration_no = models.CharField(max_length=12, verbose_name='사업자등록번호')
    company_name = models.TextField(verbose_name='상호명')
    president_name = models.TextField(verbose_name='대표자명')
    company_condition = models.TextField(verbose_name='업태') 
    company_line = models.TextField(verbose_name='종목')
    company_introduction = models.TextField(verbose_name='회사소갸')

class SuppliersUsers(models.Model):
    user_id #?
    supplier_code = models.CharField(max_length=8, verbose_name='공급사 코드')
    supplier_namesupplier_name = models.CharField(max_length=100, verbose_name='공급사명')
    permission_category_select = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='상품 등록 시 분류선택 권한')
    permission_product_modify = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='상품 수정 권한')
    permission_product_display = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='상품 진열 권한')
    permission_product_selling = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='상품 판매 권한')
    permission_product_delete = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='등록 상품 삭제 권한')
    permission_board_manage = models.CharField(max_length=1, choices=(
        ('T','허용함'),
        ('F','허용안함')
    ), verbose_name='게시판 권한 설정')
    user_name = models.TextField(verbose_name='공급사운영자명')
    nick_name #?
    nick_name_icon_type #?
    nick_name_icon_url #?
    use_nick_name_icon #?
    use_writer_name_icon #?
    email = models.EmailField(verbose_name='이메일')
    phone = models.TextField(verbose_name='전화번호')
    permission_shop_no = models.IntegerField(verbose_name='접근가능 쇼핑몰')
    permitted_category_list #?