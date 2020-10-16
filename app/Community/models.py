from django.db import models

# Create your models here.
class Boards(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    board_no = models.IntegerField(verbose_name='게시판 번호')
    board_type = models.IntegerField(choices=(
        (1,'운영'),
        (2,'일반'),
        (3,'자료실'),
        (4,'기타'),
        (5,'상품'),
        (6,'갤러리'),
        (7,'1:1 상담'),
        (11,'한줄메모')
    ), verbose_name='게시판 분류')
    board_name = models.TextField(verbose_name='게시판 이름')
    use_additional_board = models.CharField(max_length=1, choices=(
        ('T','추가게시판'),
        ('F','기본게시판')
    ), verbose_name='게시판 추가여부')
    use_board = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='게시판 사용여부')
    use_display = models.CharField(max_length=1, choices=(
        ('T','표시함'),
        ('F','표시안함')
    ), verbose_name='표시여부')
    display_order #?

class BoardsArticles(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    article_no = models.IntegerField(verbose_name='게시물 번호')
    parent_article_no = models.IntegerField(verbose_name='부모 게시물 번호')
    board_no = models.IntegerField(verbose_name='게시판 번호')
    product_no = models.IntegerField(verbose_name='상품 번호')
    category_no = models.IntegerField(verbose_name='분류 번호')
    board_category_no = models.IntegerField(verbose_name='게시판 카테고리 ㅓㅂㄴ호')
    reply_sequence #?
    reply_depth = models.IntegerField(verbose_name='답변 차수')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    writer = models.TextField(verbose_name='작성자명')
    writer_email = models.EmailField(verbose_name='작성자 이메일')
    member_id = models.TextField(verbose_name='회원아이디')
    title = models.TextField(verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    client_ip = models.IPAddressField(verbose_name='작성자 IP')
    nick_name = models.TextField(verbose_name='별명')
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], verbose_name='평점')
    reply_mail = models.CharField(max_length=1, choices=(
        ('Y','사용함'),
        ('N','사용안함')
    ), verbose_name='1:1 게시판 문의내용에 대한 답변 메일 여부')
    display = models.CharField(max_length=1, choices=(
        ('T','게시함'),
        ('F','게시안함')
    ), verbose_name='게시 여부')
    secret = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='비밀글 여부')
    notice = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='공지 여부')
    fixed = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='고정글 여부')
    deleted = models.CharField(max_length=1, choices=(
        ('T','삭제'),
        ('F','비삭제')
    ), verbose_name='삭제 구분')
    input_channel = models.CharField(max_length=1, choices=(
        ('P','PC'),
        ('M','모바일')
    ), verbose_name='게시물 작성 경로')
    order_id = models.TextField(verbose_name='주문번호')
    attach_file_urls #?
    hit = models.IntegerField(verbose_name='조회수')
    reply = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='1:1 게시판 문의내용에 대한 답변여부')
    reply_user_id = models.TextField(verbose_name='처리중 또는 답변완료 한 운영자 아이디')
    reply_status = models.CharField(max_length=1, choices=(
        ('N','답변전'),
        ('P','처리중'),
        ('C','처리완료')
    ), verbose_name='답변 처리 상태')
    naverpay_review_id = models.TextField(verbose_name='네이버페이 리뷰 아이디')
    display_time #?
    display_time_start_hour #?
    display_time_end_hour #?
    attached_file_detail #?
    attached_file_urls #?

class BoardsArticlesComments(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    board_no = models.IntegerField(verbose_name='게시판 번호')
    article_no = models.IntegerField(verbose_name='게시물 번호')
    comment_no = models.IntegerField(verbose_name='댓글 번호')
    content = models.TextField(verbose_name='댓글 내용')
    writer = models.CharField(max_length=100, verbose_name='작성자명')
    member_id = models.CharField(max_length=20, verbose_name='회원아이디')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    client_ip = models.IPAddressField(verbose_name='작성자 IP')
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], verbose_name='평점')
    secret = models.CharField(max_length=1, choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='비밀글 여부')
    parent_comment_no = models.IntegerField(verbose_name='부모 댓글 번호')
    input_channel =  = models.CharField(max_length=1, choices=(
        ('P','PC'),
        ('M','모바일')
    ), verbose_name='쇼핑몰 구분')

class CustomersReviews(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    product_no = models.IntegerField(verbose_name='상품 번호')
    review_no = models.IntegerField(verbose_name='리뷰 번호')
    order_id = models.IntegerField(verbose_name='주문 번호')
    nickname = models.TextField(verbose_name='작성자 별명')
    title = models.TextField(verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    content_text_length = models.IntegerField(verbose_name='리뷰 길이')
    input_channel = models.CharField(max_length=1, choices=(
        ('P','PC'),
        ('M','모바일')
    ), verbose_name='리뷰 작성 경로')
    writer = models.TextField(verbose_name='작성자명')
    writing_id = models.TextField(verbose_name='작성자아이디')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    comment_count = models.IntegerField(verbose_name='답변 개수')
    like_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='좋아요 개수')
    share_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='공유 개수')
    hit_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='조회수')
    additional_information #?
    images #?
    tags #?
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], verbose_name='평점')
    use_share = models.CharField(max_length=1,choices=(
        ('T','공유함'),
        ('F','공유안함')
    ), verbose_name='리뷰 SNS 공유여부')
    display = models.CharField(max_length=1,choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='리뷰 게시여부')
    deleted = models.CharField(max_length=1,choices=(
        ('T','삭제함'),
        ('F','삭제안함')
    ), verbose_name='리뷰 삭제여부')

class Reviews(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    product_no = models.IntegerField(verbose_name='상품 번호')
    review_no = models.IntegerField(verbose_name='리뷰 번호')
    order_id = models.IntegerField(verbose_name='주문 번호')
    nickname = models.TextField(verbose_name='작성자 별명')
    title = models.TextField(verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    content_text_length = models.IntegerField(verbose_name='리뷰 길이')
    input_channel = models.CharField(max_length=1, choices=(
        ('P','PC'),
        ('M','모바일')
    ), verbose_name='리뷰 작성 경로')
    writer = models.TextField(verbose_name='작성자명')
    writing_id = models.TextField(verbose_name='작성자아이디')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    comment_count = models.IntegerField(verbose_name='답변 개수')
    like_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='좋아요 개수')
    share_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='공유 개수')
    hit_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='조회수')
    additional_information #?
    images #?
    tags #?
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], verbose_name='평점')
    use_share = models.CharField(max_length=1,choices=(
        ('T','공유함'),
        ('F','공유안함')
    ), verbose_name='리뷰 SNS 공유여부')
    display = models.CharField(max_length=1,choices=(
        ('T','사용함'),
        ('F','사용안함')
    ), verbose_name='리뷰 게시여부')
    deleted = models.CharField(max_length=1,choices=(
        ('T','삭제함'),
        ('F','삭제안함')
    ), verbose_name='리뷰 삭제여부')

class ReviewsComments(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    review_no = models.IntegerField(verbose_name='리뷰 번호')
    comment_no = models.IntegerField(verbose_name='댓글 번호')
    content = models.TextField(verbose_name='내용')
    writer = models.TextField(verbose_name='작성자명')
    nickname = models.TextField(verbose_name='작성자 별명')
    ip = models.IPAddressField(verbose_name='작성자 IP')
    writing_id = models.TextField(verbose_name='작성자아이디')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
