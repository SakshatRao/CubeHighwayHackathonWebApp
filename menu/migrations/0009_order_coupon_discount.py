# Generated by Django 3.1.7 on 2021-03-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_auto_20210320_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.FloatField(default=0),
        ),
    ]
