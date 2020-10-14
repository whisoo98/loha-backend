from django.db import models

# Create your models here.
## !Complete!
class Benefits(models.Model):
shop_no
benefit_no
use_benefit
benefit_name
benefit_division
benefit_type
use_benefit_period
benefit_start_date
benefit_end_date
platform_types
use_group_binding
customer_group_list
product_binding_type
use_except_category
available_coupon
icon_url
created_date
period_sale
repurchase_sale
bulk_purchase_sale
member_sale
new_product_sale
shipping_fee_sale
gift
gift_product_bundle

class Coupons(models.Model):
 shop_no
coupon_no
coupon_type
coupon_name
coupon_description
created_date
deleted
is_stopped_issued_coupon
pause_begin_datetime
pause_end_datetime
benefit_text
benefit_type
benefit_price
benefit_percentage
benefit_percentage_round_unit
benefit_percentage_max_price
include_regional_shipping_rate
include_foreign_delivery
coupon_direct_url
issue_type
issue_sub_type
issue_member_join
issue_member_join_recommend
issue_member_join_type
issue_order_amount_type
issue_order_start_date
issue_order_end_date
issue_order_amount_limit
issue_order_amount_min
issue_order_amount_max
issue_order_path
issue_order_type
issue_order_available_product
issue_order_available_category
issue_anniversary_type
issue_anniversary_pre_issue_day
issue_module_type
issue_review_count
issue_review_has_image
issue_quantity_min
issue_quntity_type
issue_max_count
issue_max_count_by_user
issue_count_per_once
issued_count
issue_member_group_no
issue_member_group_name
issue_no_purchase_period
issue_reserved
issue_reserved_date
available_date
available_period_type
available_begin_datetime
available_end_datetime
available_site
available_scope
available_day_from_issued
available_price_type
available_min_price
available_amount_type
available_payment_method
available_product
available_product_list
available_category
available_category_list
available_coupon_count_by_order
serial_generate_method
coupon_image_type
coupon_image_path
show_product_detail
use_notification_when_login
send_sms_for_issue
send_email_for_issue
discount_amount
discount_rate

class CouponsIssues(models.Model):
shop_no
coupon_no
member_id
group_no
issued_date
expiration_date
used_coupon
used_date
related_order_id
count

class CustomersCoupons(models.Model):
shop_no
coupon_no
issue_no
coupon_name
available_price_type
available_price_type_detail
available_min_price
available_payment_methods
benefit_type
benefit_price
benefit_percentage
benefit_percentage_round_unit
benefit_percentage_max_price
credit_amount
issued_date
available_begin_datetime
available_end_datetime

