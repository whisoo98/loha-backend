from django.db import models

# Create your models here.
class CustomersPrivacy(models.Model):
shop_no
member_id
name
name_english
name_phonetic
phone
cellphone
email
sms
news_mail
wedding_anniversary
birthday
solar_calendar
total_points
available_points
used_points
city
state
address1
address2
group_no
job_class
job
zipcode
created_date
member_authentication
use_blacklist
pointfy_member
blacklist_type
last_login_date
member_authority
nick_name
recommend_id
residence
interest
gender
member_type
company_type
foreigner_type
lifetime_member
corporate_name
nationality
shop_name
country_code
use_mobile_app
join_path
fixed_group
available_credits
additional_information

class ProductsWishlistCustomers(models.Model):
shop_no
member_id