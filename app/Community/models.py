from django.db import models

# Create your models here.
class Boards(models.Model):
shop_no
board_no
board_type
board_name
use_additional_board
use_board
use_display
display_order

class BoardsArticles(models.Model):
shop_no
article_no
parent_article_no
board_no
product_no
category_no
board_category_no
reply_sequence
reply_depth
created_date
writer
writer_email
member_id
title
content
client_ip
nick_name
rating
reply_mail
display
secret
notice
fixed
deleted
input_channel
order_id
attach_file_urls
hit
reply
reply_user_id
reply_status
naverpay_review_id
display_time
display_time_start_hour
display_time_end_hour
attached_file_detail
attached_file_urls

class BoardsArticlesComments(models.Model):
shop_no
board_no
article_no
comment_no
content
writer
member_id
created_date
client_ip
rating
secret
parent_comment_no
input_channel

class CustomersReviews(models.Model):
shop_no
product_no
review_no
order_id
nickname
title
content
content_text_length
input_channel
writer
writing_id
created_date
comment_count
like_count
share_count
hit_count
additional_information
images
tags
rating
use_share
display
deleted

class Reviews(models.Model):
shop_no
product_no
review_no
order_id
nickname
title
content
content_text_length
input_channel
writer
writing_id
created_date
comment_count
like_count
share_count
hit_count
additional_information
images
tags
rating
use_share
display
deleted

class ReviewsComments(models.Model):
shop_no
review_no
comment_no
content
writer
nickname
ip
writing_id
created_date
