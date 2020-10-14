from django.db import models

# Create your models here.
## !Complete!
class MetaProducts(models.Model):
    shop_no
    product_code
    custom_product_code
    product_name
    eng_product_name
    supply_product_name
    internal_product_name
    model_name
    display
    selling
    product_condition
    product_used_month
    summary_description
    product_tag
    price_content
    buy_limit_by_product
    buy_limit_type
    repurchase_restriction
    single_purchase_restriction
    points_by_product
    except_member_points
    detail_image
    list_image
    tiny_image
    small_image
    use_naverpay
    naverpay_type
    icon_show_period
    icon
    hscode
    product_weight
    product_material
    created_date
    updated_date
    english_product_material
    cloth_fabric
    list_icon
    sold_out
    decorationimages
    benefits
    additionalimages
    category
    project_no
    description
    separated_mobile_description
    additional_image
    payment_info
    shipping_info
    exchange_info
    service_info
    country_hscode
    simple_description
    shipping_fee_by_product
    shipping_method
    prepaid_shipping_fee
    shipping_period
    shipping_scope
    shipping_area
    shipping_fee_type
    shipping_rates
    clearance_category_eng
    clearance_category_kor
    clearance_category_code
    additional_information
    image_upload_type
    main
    relational_product
    memos
    hits
    seo
    tags

    class Meta:
        abstract = True

class Products(MetaProducts):
    product_no
    price_excluding_tax
    price
    retail_price
    supply_price
    margin_rate
    tax_type
    tax_amount
    buy_unit_type
    buy_unit
    order_quantity_limit_type
    minimum_quantity
    maximum_quantity
    points_setting_by_paymen
    points_amount
    product_volume
    adult_certification
    has_option
    option_type
    manufacturer_code
    trend_code
    brand_code
    supplier_code
    made_date
    release_date
    origin_classification
    origin_place_no
    origin_place_value
    made_in_code
    select_one_by_option
    approve_status
    classification_code
    additional_price
    discountprice
    options
    variants
    mobile_description
    product_tax_type_text
    set_product_type
    origin_place_code


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_product'
        verbose_name = '상품'
        vebose_name_plural = '상품'

class BundleProducts(MetaProducts):
    product_no
    bundle_product_components
    points_setting_by_payment
    points_amount
    adult_certification
    discountprice
    bundle_product_sales
    mobile_description

class CategoriesProducts(models.Model):
shop_no
product_no
sequence_no
auto_sort
sold_out
fixed_sort
not_for_sale
display_group
sequence

class MainsProducts(models.Model):
shop_no
product_no
product_name
fixed_sort

class ProductsAddtionalImages(models.Model):
shop_no
additional_image

class ProductsApprove(models.Model):
shop_no
status
product_no

class ProductsDecorationImages(models.Model):
code
path
shop_no
use_show_date
show_start_date

show_end_date

image_list

class ProductsDiscountPrice(models.Model):
pc_discount_price
mobile_discount_price

class ProductsIcons(models.Model):
code
path
shop_no
use_show_date
show_start_date

show_end_date

image_list

class ProductsImages(models.Model):
path
shop_no
product_no
detail_image
list_image
tiny_image
small_image

class ProductsMemos(models.Model):
memo_no
author_id
created_date

memo

class ProductsOptions(models.Model):
shop_no
product_no
has_option
option_type
option_list_type
option_preset_code
options
select_one_by_option
option_preset_name
use_additional_option
additional_options
use_attached_file_option
attached_file_option

class ProductsSeo(models.Model):
shop_no
meta_title
meta_author
meta_description
meta_keywords
meta_alt
search_engine_exposure

class ProductsTags(models.Model):
shop_no
tag
product_no

class ProductsVariants(models.Model):
shop_no
variant_code
options
custom_variant_code
display
selling
additional_amount
use_inventory
important_inventory
inventory_control_type
display_soldout
quantity
safety_inventory
inventories
duplicated_custom_variant_code
product_no

class ProductsVariantsInventories(models.Model):
shop_no
variant_code
use_inventory
important_inventory
inventory_control_type
display_soldout
quantity
safety_inventory

   