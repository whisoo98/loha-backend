# Generated by Django 3.1.6 on 2021-04-03 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20210308_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediastream',
            name='product_id',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='mediastream',
            name='push_count',
            field=models.IntegerField(default=0),
        ),
    ]
