from django.db import models

# Create your models here.
## !Complete!
class CustomersInviation(models.Model):
shop_no
member_id

class Sms(models.Model):
queue_code

class SmsSenders(models.Model):
sender_no
sender
auth_status