# Generated by Django 4.1.5 on 2023-02-21 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_products_product_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BillsAndSales', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='house',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='landmark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='paymentMethod',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(blank=True, default='cart', max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('itemcount', models.CharField(blank=True, max_length=255, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
    ]