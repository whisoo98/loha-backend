from django.db import models


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    cafe24_user_id = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created']

