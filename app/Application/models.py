from django.db import models

# Create your models here.
## !Complete!
class Apps(models.Model):
version
version_expiration_date
initial_version
previous_version

class AppstoreOrders(models.Model):
    order_id
order_name
order_amount
currency
return_url
automatic_payment
created_date
confirmation_url

class AppstorePayments(models.Model):
order_id
payment_status
title
approval_no
payment_gateway_name
payment_method
payment_amount
refund_amount
currency
locale_code
automatic_payment
pay_date
refund_date
expiration_date
class ScriptTags(models.Model):
shop_no
script_no
client_id
src
display_location
exclude_path
skin_no
created_date
updated_date