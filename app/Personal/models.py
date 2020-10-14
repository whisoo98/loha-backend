from django.db import models

## !Complete!
class Carts(models.Model):
shop_no
basket_product_no
member_id
created_date

product_no
additional_option_values
variant_code
quantity
product_price
option_price
product_bundle
shipping_type
category_no

class CustomersWishlist(models.Model):
shop_no
wishlist_no
product_no
variant_code
additional_option
attached_file_option
price
product_bundle
created_date

price_content

class ProductsCarts(models.Model):
shop_no
member_id
created_date

product_no
variant_code
quantity
product_bundle