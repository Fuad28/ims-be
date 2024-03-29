# Generated by Django 4.1.7 on 2024-01-09 21:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0020_productitem_eoq_productitem_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productitem",
            name="status",
        ),
        migrations.AddField(
            model_name="productitem",
            name="annual_demand",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="productitem",
            name="last_forcast",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
