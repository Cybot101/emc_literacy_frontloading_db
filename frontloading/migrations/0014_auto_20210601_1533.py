# Generated by Django 3.2.2 on 2021-06-01 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontloading', '0013_auto_20210601_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='etymology',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='word',
            name='parts',
            field=models.CharField(default='', max_length=200),
        ),
    ]