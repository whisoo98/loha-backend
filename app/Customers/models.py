from django.db import models

# Create your models here.
class CustomerGroups(models.Model):
shop_no
group_no
group_name
group_description
benefits_paymethod
buy_benefits
ship_benefits
product_availability
discount_information
points_information
mobile_discount_information
mobile_points_information

class CustomerGroupsCustomers(models.Model):
shop_no
group_no
member_id
fixed_group

class Customers(models.Model):
shop_no
member_id
group_no
member_authentication
use_blacklist
blacklist_type
sms
news_mail
solar_calendar
total_points
available_points
used_points
pointfy_member
last_login_date
gender
use_mobile_app
available_credits
created_date
fixed_group

class CustomersMeomos(models.Model):
shop_no
memo_no
author_id
memo
important_flag
created_date

class CustomersPaymentInformation(models.Model):
shop_no
member_id
payment_method
payment_gateway
created_date

    