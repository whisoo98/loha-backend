# Generated by Django 2.2.16 on 2021-01-26 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_streamer',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='room_name',
            field=models.ForeignKey(db_column='room', db_index=False, on_delete=django.db.models.deletion.CASCADE, to='chat.Room'),
        ),
    ]
