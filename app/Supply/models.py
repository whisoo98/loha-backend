from django.db import models

# Create your models here.
## !Complete!
class Suppliers(models.Model):
shop_no
supplier_code
supplier_name
status
commission
payment_period
business_item
payment_type
supplier_type
use_supplier
created_date

updated_date

country_code
zipcode
address1
address2
manager_information
trading_type
payment_method
payment_start_day
payment_end_day
payment_start_date
payment_end_date
bank_code
bank_code
bank_account_no
bank_account_name
phone
fax
market_country_code
market_zipcode
market_address1
market_address2
exchange_country_code
exchange_zipcode
exchange_address1
exchange_address2
homepage_url
mall_url
account_start_date
account_stop_date
show_supplier_info
memo
company_registration_no
company_name
president_name
company_condition
company_line
company_introduction

class SuppliersUsers(models.Model):
user_id
supplier_code
supplier_name
permission_category_select
permission_product_modify
permission_product_display
permission_product_selling
permission_product_delete
permission_board_manage
user_name
nick_name
nick_name_icon_type
nick_name_icon_url
use_nick_name_icon
use_writer_name_icon
email
phone
permission_shop_no
permitted_category_list