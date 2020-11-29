from django.db import models


# Create your models here.

class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    prod_id = models.IntegerField(verbose_name='상품번호')
    vodurl = models.URLField(verbose_name='VOD url')



    class Meta:
        ordering = ['created']

