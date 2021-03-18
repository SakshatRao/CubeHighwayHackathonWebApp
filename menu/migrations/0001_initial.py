# Generated by Django 3.1.7 on 2021-03-18 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('description', models.TextField(default='')),
                ('image', models.ImageField(upload_to='food_imgs/')),
                ('rating', models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0)),
                ('is_veg', models.BooleanField(default=True)),
                ('food_category', models.CharField(choices=[('ST', 'Starters'), ('MC', 'Main Course'), ('DE', 'Dessert')], default='MC', max_length=10)),
                ('ingredients', models.TextField(default='')),
                ('price', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('total', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('is_paid', models.BooleanField(default=False)),
                ('final_amt', models.FloatField(default=0)),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=0)),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.fooditem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.order')),
            ],
        ),
    ]