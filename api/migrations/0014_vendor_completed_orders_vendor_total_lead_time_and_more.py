# Generated by Django 4.1.7 on 2023-11-26 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_alter_vendor_qdp_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="completed_orders",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="vendor",
            name="total_lead_time",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_cost_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="qty_ordered",
            field=models.IntegerField(),
        ),
    ]
