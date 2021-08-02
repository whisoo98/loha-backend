from django.db import models


class DeletedOrder(models.Model):
    order_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.order_id
