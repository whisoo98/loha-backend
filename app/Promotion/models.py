from django.db import models

# Create your models here.
## !Complete!
class Benefits(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    benefit_no = models.IntegerField(verbose_name='혜택 번호')
    use_benefit #?
    benefit_name = models.CharField(max_length=255, verbose_name='혜택명')
    benefit_division #?
    benefit_type #?
    use_benefit_period #?
    benefit_start_date = models.DateTimeField(auto_now_add=True, verbose_name='혜택 시작일')
    benefit_end_date = models.DateTimeField(verbose_name='혜택 종료일')
    platform_types #?
    use_group_binding #?
    customer_group_list #?
    product_binding_type #?
    use_except_category #?
    available_coupon #?
    icon_url #?
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='혜택 등록일')
    period_sale #?
    repurchase_sale #?
    bulk_purchase_sale #?
    member_sale #?
    new_product_sale #?
    shipping_fee_sale #?
    gift #?
    gift_product_bundle #?

class Coupons(models.Model):
    shop_no = models.IntegerField(default=1, verbose_name='멀티쇼핑몰 번호')
    coupon_no = models.IntegerField(verbose_name='쿠폰 번호')
    coupon_type = models.CharField(max_length=1, choices=(
        ('O','온라인 쿠폰'),
        ('S','오프라인 시리얼 쿠폰')
    ), verbose_name='쿠폰유형')
    coupon_name = models.TextField(verbose_name='쿠폰명')
    coupon_description = models.TextField(verbose_name='쿠폰설명')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    deleted = models.CharField(max_length=1, choices=(
        ('T','삭제'),
        ('F','삭제되지 않음')
    ), verbose_name='쿠폰삭제 여부')
    is_stopped_issued_coupon = models.CharField(max_length=1, choices=(
        ('T','완전삭제'),
        ('F','완전삭제 아님')
    ), verbose_name='쿠폰 완전삭제 (발급된 쿠폰 사용정지) 여부')
    pause_begin_datetime = models.DateField(verbose_name='쿠폰 발급 일시정지 시작시간')
    pause_end_datetime = models.DateField(verbose_name='쿠폰 발급 일시정지 종료시간')
    benefit_text = models.TextField(verbose_name='쿠폰혜택 상세내역 출력')
    benefit_type #?
    benefit_price = models.IntegerField(verbose_name='혜택 금액')
    benefit_percentage = models.IntegerField(verbose_name='혜택 비율')
    benefit_percentage_round_unit = models.IntegerField(verbose_name='혜택 비율 절사 단위')
    benefit_percentage_max_price = models.IntegerField(verbose_name='혜택 비율 최대 금액')
    include_regional_shipping_rate = models.CharField(max_length=1, choices=(
        ('T','지역별 구분 포함'),
        ('F','지역별 구분 미포함')
    ), default='F', verbose_name='배송비 할인 시 지역별 구분 포함 여부')
    include_foreign_delivery = models.CharField(max_length=1, choices=(
        ('T','지역별 구분 포함'),
        ('F','지역별 구분 미포함')
    ), default='F', verbose_name='해외배송 포함여부')
    coupon_direct_url #URL
    issue_type #?
    issue_sub_type = models.CharField(max_length=1, choices=(
        ('M','회원 대상'),
        ('C','실시간 접속자 대상'),
        ('J','회원 가입'),
        ('D','배송 완료 시'),
        ('A','기념일(생일)'),
        ('I','모듈(프로그램) 설치'),
        ('P','상품 후기 작성'),
        ('O','주문 완료 시'),
        ('Q','구매 수량 충족 시'),
        ('F','첫 구매 고객'),
        ('N','일정기간 미구매 회원 대상')
    ), verbose_name='발급 하위 유형')
    issue_member_join = models.CharField(max_length=1, choices=(
        ('T','발급 대상'),
        ('F','발급 대상 아님')
    ), default='F', verbose_name='회원가입시 쿠폰 발급 여부')
    issue_member_join_recommend = models.CharField(max_length=1, choices=(
        ('T','발급 대상'),
        ('F','발급 대상 아님')
    ), default='F', verbose_name='회원가입시 추천인에게 쿠폰 발급 여부')
    issue_member_join_type = models.CharField(max_length=1, choices=(
        ('A','SMS 수신동의 AND 이메일 수신동의'),
        ('O','SMS 수신동의 OR 이메일 수신동의'),
        ('S','SMS 수신동의'),
        ('E','이메일 수신동의')
    ), verbose_name='회원가입시 쿠폰 발급 대상')
    issue_order_amount_type = models.CharField(max_length=1, choices=(
        ('O','구매금액 기준'),
        ('S','실결제 금액기준')
    ), verbose_name='발급가능 구매금액 유형')
    issue_order_start_date = models.DateField(verbose_name='쿠폰발급 가능한 주문시작일시')
    issue_order_end_date = models.DateField(verbose_name='쿠폰발급 가능한 주문종료일시')
    issue_order_amount_limit = models.CharField(max_length=1, choices=(
        ('U','제한 없음'),
        ('L','최소 금액'),
        ('S','금액 범위')
    ), verbose_name='발급 가능 구매 금액 제한 유형')
    issue_order_amount_min = models.IntegerField(verbose_name='발급 가능 최소 구매 금액')
    issue_order_amount_max = models.IntegerField(verbose_name='발급 가능 최대 구매 금액')
    issue_order_path #?
    issue_order_type = models.CharField(max_length=1, choices=(
        ('O','주문서단위 발급쿠폰'),
        ('P','상품단위 발급쿠폰')
    ), verbose_name='발급단위')
    issue_order_available_product = models.CharField(max_length=1, choices=(
        ('U','제한 없음'),
        ('I','선택 상품 적용'),
        ('E','선택 상품 제외')
    ), verbose_name='발급 대상 상품')
    issue_order_available_category = models.CharField(max_length=1, choices=(
        ('U','제한 없음'),
        ('I','선택 상품 적용'),
        ('E','선택 상품 제외')
    ), verbose_name='발급 대상 카테고리')
    issue_anniversary_type = models.CharField(max_length=1, choices=(
        ('B','생일'),
        ('W','결혼 기념일')
    ), verbose_name='발급 조건 기념일 유형')
    issue_anniversary_pre_issue_day #?
    issue_module_type = models.CharField(max_length=1, choices=(
        ('S','바로가기'),
        ('B','즐겨찾기'),
        ('L','라이브링콘')
    ), verbose_name='발급 조건 설치 모듈 유형')
    issue_review_count = models.IntegerField(verbose_name='발급 조건 상품 후기 개수')
    issue_review_has_image = models.CharField(max_length=1, choices=(
        ('T','포함'),
        ('F','미포함')
    ), default='F', verbose_name='발급 조건 상품 후기 이미지 포함 여부')
    issue_quantity_min = models.IntegerField(verbose_name='쿠폰 발급가능 최소구매수량')
    issue_quntity_type = models.CharField(max_length=1, choices=(
        ('P','상품 수량 기준'),
        ('O','주문 수량 기준')
    ), verbose_name='쿠폰 발급가능수량 판단기준')
    issue_max_count = models.IntegerField(verbose_name='최대 발급수')
    issue_max_count_by_user = models.IntegerField(verbose_name='동일 사용자 당 최대 발급수')
    issue_count_per_once = models.IntegerField(verbose_name='쿠폰발급 회당 발급수량 (1회 발급수량)')
    issued_count = models.IntegerField(verbose_name='발급된 수량')
    issue_member_group_no = models.IntegerField(verbose_name='발급대상 회원등급 번호')
    issue_member_group_name = models.TextField(verbose_name='발급대상 회원등급 이름')
    issue_no_purchase_period #?
    issue_reserved = models.CharField(max_length=1, choices=(
        ('T','자동 발행 예약 사용'),
        ('F','자동 발행 예약 미사용')
    ), default = 'F', verbose_name='자동 발행 예약 사용 여부')
    issue_reserved_date = models.DateTimeField(verbose_name='자동 발행 예약 발급 일시')
    available_date #?
    available_period_type #?
    available_begin_datetime #?
    available_end_datetime #?
    available_site #?
    available_scope #?
    available_day_from_issued #?
    available_price_type = models.CharField(max_length=1, choices=(
        ('U','제한 없음'),
        ('O','주문 금액 기준'),
        ('P','상품 금액 기준')
    ), verbose_name='사용가능 구매 금액 유형')
    available_min_price = models.IntegerField(verbose_name='사용가능 구매 금액')
    available_amount_type #?
    available_payment_method = models.CharField(max_length=1, choices=(
        ('R','무통장입금'),
        ('E','가상계좌'),
        ('C','신용카드'),
        ('A','계좌이체'),
        ('H','휴대폰'),
        ('M','적립금'),
        ('K','케이페이'),
        ('P','페이나우'),
        ('N','페이코'),
        ('O','카카오페이'),
        ('S','스마일페이'),
        ('V','네이버페이'),
        ('B','편의점'),
        ('D','토스')
    ), verbose_name='사용가능 결제수단')
    available_product #?
    available_product_list #?
    available_category #?
    available_category_list #?
    available_coupon_count_by_order = models.IntegerField(verbose_name='주문서 당 동일쿠폰 최대 사용 수')
    serial_generate_method = models.CharField(max_length=1, choices=(
        ('A','자동 생성'),
        ('M','직접 등록'),
        ('E','엑셀 업로드')
    ),verbose_name='시리얼 쿠폰 생성방법')
    coupon_image_type = models.CharField(max_length=1, choices=(
        ('B','기본 이미지 사용'),
        ('C','직접 업로드')
    ),verbose_name='쿠폰 이미지 유형')
    coupon_image_path #URL
    show_product_detail = models.CharField(max_length=1, choices=(
        ('T','상품상세페이지 노출'),
        ('F','상품상세페이지 미노출')
    ), default='F', verbose_name='상품상세페이지 노출여부')
    use_notification_when_login = models.CharField(max_length=1, choices=(
        ('T','알람 노출'),
        ('F','알람 미노출')
    ), default='F', verbose_name='로그인 시 쿠폰발급 알람 사용여부')
    send_sms_for_issue = models.CharField(max_length=1, choices=(
        ('T','SMS 발송'),
        ('F','SMS 미발송')
    ), default='F', verbose_name='쿠폰발급 SMS 발송 여부')
    send_email_for_issue = models.CharField(max_length=1, choices=(
        ('T','이메일 발송'),
        ('F','이메일 미발송')
    ), default='F', verbose_name='쿠폰 발급정보 이메일 발송여부')
    discount_amount = models.IntegerField(verbose_name='할인금액')
    discount_rate = models.IntegerField(verbose_name='할인율')

class CouponsIssues(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    coupon_no = models.IntegerField(verbose_name='쿠폰 번호')
    member_id = models.TextField(verbose_name='회원아이디')
    group_no = models.IntegerField(verbose_name='발급대상 회원등급 번호')
    issued_date = models.DateTimeField(verbose_name='쿠폰 발급일자')
    expiration_date = models.DateTimeField(verbose_name='만료일')
    used_coupon #?
    used_date = models.DateTimeField(verbose_name='쿠폰 사용 일자')
    related_order_id = models.IntegerField(verbose_name='관련 주문번호')
    count = models.IntegerField(verbose_name='카운트')

class CustomersCoupons(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    coupon_no = models.IntegerField(verbose_name='쿠폰 번호')
    issue_no = models.IntegerField(verbose_name='쿠폰 발급번호')
    coupon_name = models.TextField(verbose_name='쿠폰명')
    available_price_type = models.CharField(max_length=1, choices=(
        ('U','제한 없음'),
        ('O','주문 금액 기준'),
        ('P','상품 금액 기준')
    ), verbose_name='사용가능 구매 금액 유형')
    available_price_type_detail = models.CharField(max_length=1, choices=(
        ('U','모든 상품의 주문 금액'),
        ('I','쿠폰 적용 상품의 주문 금액')
    ), verbose_name='사용가능 구매 금액 유형 상세')
    available_min_price = models.IntegerField(verbose_name='사용가능 구매 금액')
    available_payment_methods = models.CharField(max_length=1, choices=(
        ('R','무통장입금'),
        ('E','가상계좌'),
        ('C','신용카드'),
        ('A','계좌이체'),
        ('H','휴대폰'),
        ('M','적립금'),
        ('K','케이페이'),
        ('P','페이나우'),
        ('N','페이코'),
        ('O','카카오페이'),
        ('S','스마일페이'),
        ('V','네이버페이'),
        ('B','편의점'),
        ('D','토스')
    ), verbose_name='사용가능 결제수단')
    benefit_type = models.CharField(max_length=1, choices=(
        ('A','할인금액'),
        ('B','할인율'),
        ('C','적립금액'),
        ('D','적립율'),
        ('E','기본배송비 할인(전액할인)'),
        ('I','기본배송비 할인(할인율)'),
        ('H','기본배송비 할인(할인금액)'),
        ('F','즉시적립'),
        ('G','예치금')
    ), verbose_name='혜택 구분')
    benefit_price = models.IntegerField(verbose_name='혜택 금액')
    benefit_percentage = models.IntegerField(verbose_name='혜택 비율')
    benefit_percentage_round_unit = models.IntegerField(verbose_name='혜택 비율 절사 단위')
    benefit_percentage_max_price = models.IntegerField(verbose_name='혜택 비율 최대 금액')
    credit_amount = models.IntegerField(verbose_name='예치금 지급 금액')
    issued_date = models.DateTimeField(verbose_name='발행일')
    available_begin_datetime = models.DateTimeField(verbose_name='사용 기간 시작 일시')
    available_end_datetime = models.DateTimeField(verbose_name='사용 기간 종료 일시')

