# Generated by Django 4.1.5 on 2023-02-22 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BillsAndSales', '0006_billfinal_billcalculations_billid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billcalculations',
            name='gst',
        ),
        migrations.RemoveField(
            model_name='billcalculations',
            name='totalprice',
        ),
    ]
