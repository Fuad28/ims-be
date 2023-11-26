# Generated by Django 4.1.7 on 2023-11-26 09:56

from django.db import migrations, models
import django.db.models.deletion

def set_default_size_category(apps, schema_editor):
    ProductItem = apps.get_model('api', 'ProductItem')
    Business = apps.get_model('api', 'Business')
    SizeCategory = apps.get_model('api', 'SizeCategory')

    default_business, created = Business.objects.get_or_create(name='Default business', email= "defaultbusiness@business.com")
    default_size_category, created = SizeCategory.objects.get_or_create(name='Large', business= default_business)
    ProductItem.objects.filter(size_category=None).update(size_category=default_size_category)

class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_remove_productsizecategory_business_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productitem",
            name="size_category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_items",
                to="api.sizecategory",
            ),
            preserve_default=False,
        ),

        migrations.RunPython(set_default_size_category)
    ]