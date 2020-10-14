from django.db import models

# Create your models here.
## !Complete!
class Brands(models.Model):
shop_no
brand_code
brand_name
use_brand
search_keyword
product_count
created_date

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_product'
        verbose_name = '상품'
        vebose_name_plural = '상품'

class Classifications(models.Model):
shop_no
classification_code
classification_name
classification_description
use_classification
created_date

product_count

class Manufacturers(models.Model):
shop_no
manufacturer_code
manufacturer_name
president_name
use_manufacturer
email
phone
homepage
zipcode
address1
address2
created_date


class Oringin(models.Model):
origin_place_no
origin_place_name
foreign
made_in_code

class Trends(models.Model):
shop_no
trend_code
trend_name
use_trend
created_date

product_count