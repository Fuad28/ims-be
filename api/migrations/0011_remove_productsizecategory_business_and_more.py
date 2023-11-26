# Generated by Django 4.1.7 on 2023-11-26 09:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_rename_cost_price_order_total_cost_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productsizecategory",
            name="business",
        ),
        migrations.RemoveField(
            model_name="productsizecategory",
            name="product",
        ),
        migrations.CreateModel(
            name="SizeCategory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="api.business",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="api.business",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="productitem",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_items",
                to="api.category",
            ),
        ),
        migrations.AlterField(
            model_name="productitem",
            name="size_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_items",
                to="api.sizecategory",
            ),
        ),
        migrations.DeleteModel(
            name="ProductCategory",
        ),
        migrations.DeleteModel(
            name="ProductSizeCategory",
        ),
    ]
