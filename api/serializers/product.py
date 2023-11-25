from rest_framework import serializers

from api.models import Product, ProductCategory, ProductItem, ProductSizeCategory
from api.serializers.vendor import SimpleVendorSerializer

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "image", "quanitty"]



class ProductCategorySerializer(serializers.ModelSerializer):
    product= ProductSerializer()

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "product"]



class ProductSizeCategorySerializer(serializers.ModelSerializer):
    product= ProductSerializer()

    class Meta:
        model = ProductSizeCategory
        fields =  ["id", "name", "product"]



class ProductItemSerializer(serializers.ModelSerializer):
    product= ProductSerializer()
    size_category= ProductCategorySerializer()
    category= ProductCategorySerializer()
    vendor= SimpleVendorSerializer()

    class Meta:
        model = ProductItem
        fields = [
            "id", "quantity", "safety_stock", "reordering_point",
            "cost_price", "selling_price", "holding_cost", 
            "ordering_cost", "expiring_date", "barcode", "image"
        ]
