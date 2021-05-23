from django.db import models


class Coupon(models.Model):
    user_id = models.CharField(max_length=200)
    coupon_id = models.CharField(max_length=200)
