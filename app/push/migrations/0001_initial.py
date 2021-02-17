# Generated by Django 2.2.16 on 2021-02-17 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfluencerAlarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('influencer_id', models.CharField(max_length=200)),
                ('token', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LiveAlarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Live_id', models.CharField(max_length=200)),
                ('token', models.TextField()),
            ],
        ),
    ]
