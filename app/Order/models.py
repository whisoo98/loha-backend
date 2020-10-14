from django.db import models

# Create your models here.
class Order(models.Model):
    shop_no = models.IntegerField(verbose_name='멀티쇼핑몰 번호')
    currency=models.CharField(verbose_name='화폐단위')
    order_id = models.IntegerField(auto_created=True, verbose_name='주문번호')
    market_id = models.IntegerField()#foreign
    market_order_info = models.CharField()
    member_id = models.IntegerField()#foreign
    member_email = models.EmailField()
    member_authenticiation = models.CharField()
    billing_name = models.CharField()
    bank_code = models.CharField()
    back_code_name = models.CharField()
    payment_method = models.CharField()
    payment_method_name = models.CharField()
    payment_gateway_name = models.CharField()
    sub_payment_method_code = models.CharField()
    paid = models.CharField()
    order_date = models.DateField(auto_now_add=True)
    first_order = models.CharField()
    payment_date = models.DateField()
    order_from_mobile = models.CharField()
    use_escrow = models.CharField()
    group_no_when_ordering = models.IntegerField()
    initial_order_amount = models.IntegerField()
    actual_order_amount = models.IntegerField()
    bank_account_no = models.IntegerField()
    bank_account_owner_name = models.IntegerField()
    market_customer_id = models.IntegerField()
    payment_amount = models.IntegerField()
    cancel_date = models.DateField()
    order_place_name = models.CharField()
    order_place_id = models.IntegerField()
    payment_confirmation = models.CharField()
    commission = models.IntegerField()
    postpay = models.CharField()
    admin_additional_amount = models.IntegerField()
    additional_shipping_fee = models.IntegerField()
    international_shipping_insurance = models.IntegerField()
    additional_handling_fee = models.IntegerField()
    shipping_type = models.CharField()
    shipping_type_text = models.CharField()
    shipping_status = models.CharField()
    wished_delivery_date = models.DateField()
    wished_delivery_time = models.TimeField()
    wished_carrier_id = models.CharField()
    wished_carrier_name = models.CharField()
    return_confirmed_date = models.DateField()
    total_supply_price = models.IntegerField()
    naver_point = models.IntegerField()
    additional_order_info_list
    store_pickup = models.CharField()
    easypay_name = models.CharField()
    loan_status = models.CharField()
    subscription = models.CharField()
    items
    receivers
    buyer
    shipping_fee_detail = models.CharField()
    regional_surcharge_detail = models.CharField()
    return_
    cancellation
    exchange
    customer_group_no_when_ordering=models.IntegerField()
    benefits
    coupons
    refunds
    process_status = models.CharField()
    order_item_code




    def __str__(self):
        return self.name

    class Meta:
        db_table = 'loha-back_product'
        verbose_name = '상품'
        vebose_name_plural = '상품'
