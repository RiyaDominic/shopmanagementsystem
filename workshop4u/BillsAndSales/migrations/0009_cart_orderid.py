# Generated by Django 4.1.5 on 2023-02-22 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BillsAndSales', '0008_billfinal_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='orderId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
