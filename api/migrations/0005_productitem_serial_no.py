# Generated by Django 4.1.7 on 2023-11-25 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_saleitem_productitem_vendor_rename_sales_sale_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productitem",
            name="serial_no",
            field=models.CharField(default="#000000", max_length=10),
            preserve_default=False,
        ),
    ]
