from django.db import models

# Create your models here.
## !Complete!
class Credits(models.Model):
shop_no
issue_date

member_id
group_name
increase_amount
decrease_amount
balance
admin_id
admin_name
reason
case
order_id

class CreditsReport(models.Model):
shop_no
increase_amount
decrease_amount
credits_total

class Points(models.Model):
shop_no
case
member_id
group_name
available_points_increase
available_points_decrease
available_points_total
unavailable_points
order_date

issue_date

available_date
admin_id
admin_name
order_id
reason
amount
type_

class PointsReport(models.Model):
shop_no
available_points_increase
available_points_decrease
available_points_total
unavailable_points
unavailable_coupon_points