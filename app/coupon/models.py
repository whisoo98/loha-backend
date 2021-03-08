from django.db import models

# Create your models here.

class Coupon(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    coupon_id = models.CharField(max_length=200,)