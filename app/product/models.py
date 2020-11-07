from django.db import models


# Create your models here.

class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    cafe24_user_id = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created']

