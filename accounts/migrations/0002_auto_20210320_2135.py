# Generated by Django 3.1.7 on 2021-03-20 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='membership',
            field=models.CharField(choices=[('P', 'Platinum'), ('G', 'Gold'), ('S', 'Silver'), ('B', 'Bronze'), ('N', 'None')], default='N', max_length=3),
        ),
        migrations.AddField(
            model_name='customer',
            name='membership_disc_appl',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
