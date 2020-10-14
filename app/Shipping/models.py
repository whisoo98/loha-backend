from django.db import models

# Create your models here.
## !Complete!
class Order(models.Model):
    shop_no	
    carrier_id
    shipping_carrier_code
    shipping_carrier
    track_shipment_url
    shipping_type
    contact
    secondary_contact
    email
    default_shipping_fee
    homepage_url
    default_shipping_carrier
    shipping_fee_setting
    shipping_fee_setting_detail
    express_exception_setting
    links

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_product'
        verbose_name = '상품'
        vebose_name_plural = '상품'
