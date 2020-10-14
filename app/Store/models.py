from django.db import models

# Create your models here.
## !Complete!
class Currency(models.Model):
exchange_rate
standard_currency_code
standard_currency_symbol
shop_currency_code
shop_currency_symbol
class Dashboard(models.Model):
shop_no
daily_sales_stats
weekly_sales_stats
monthly_sales_stats
sold_out_products_count
new_members_count
board_list
class MobbileSetting(models.Model):
shop_no
use_mobile_page
use_mobile_domain_redirection

class ProductsSetting(models.Model):
shop_no
calculate_price_based_on
price_rounding_unit
price_rounding_rule

class Shops(models.Model):
shop_no
default
shop_name
language_code
language_name
currency_code
currency_name
reference_currency_code
reference_currency_name
pc_skin_no
mobile_skin_no
base_domain
primary_domain
slave_domain
active
timezone_name
date_format
time_format

class SmsSetting(models.Model):
shop_no
use_sms
exclude_unsubscriber
default_sender
unsubscribe_phone
send_method

class Store(models.Model):
shop_no
shop_name
mall_id
base_domain
primary_domain
company_registration_no
company_name
president_name
company_condition
company_line
country
zipcode
address1
address2
phone
fax
email
mall_url
mail_order_sales_registration
mail_order_sales_registration_number
missing_report_reason_type
missing_report_reason
about_us_contents
company_map_url
customer_service_phone
customer_service_email
customer_service_fax
customer_service_sms
customer_service_hours
privacy_officer_name
privacy_officer_position
privacy_officer_department
privacy_officer_phone
privacy_officer_email
contact_us_mobile
contact_us_contents

class StoreAccounts(models.Model):
shop_no
bank_account_id
bank_name
bank_code
bank_code
bank_account_no
bank_account_holder
use_account

class SubscriptionShipmentsSetting(models.Model):
shop_no
subscription_no
subscription_shipments_name
product_binding_type
product_list
category_list
use_discount
discount_value_unit
discount_values
related_purchase_quantity
subscription_shipments_cycle_type
subscription_shipments_cycle
use_order_price_condition
order_price_greater_than
include_regional_shipping_rate

class Users(models.Model):
user_id
user_name
phone
email
ip_restriction_type
admin_type
last_login_date
shop_no
nick_name
nick_name_icon_type
nick_name_icon_url
board_exposure_setting
memo
available
multishop_access_authority
menu_access_authority
detail_authority_setting
ip_access_restriction
access_permission
