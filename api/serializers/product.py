from rest_framework import serializers

from api.models import Product, ProductItem, Category
from api.serializers.general import CategorySerializer, SizeCategorySerializer
from api.serializers.vendor import SimpleVendorSerializer


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ["id", "name", "category", "image", "quantity"]

    def create(self, validated_data):
        validated_data["business"] = self.context["request"].user.business
        return super().create(validated_data)


class ProductItemSerializer(serializers.ModelSerializer):
    serial_no = serializers.CharField(max_length=10, read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = ProductItem
        fields = [
            "id",
            "serial_no",
            "status",
            "quantity",
            "eoq",
            "safety_stock",
            "reordering_point",
            "cost_price",
            "selling_price",
            "holding_cost",
            "ordering_cost",
            "expiring_date",
            "barcode",
            "image",
            "product",
            "size_category",
            "category",
            "vendor",
        ]

    def to_representation(self, instance: ProductItem):
        data = super().to_representation(instance)

        if instance.product:
            data["product"] = ProductSerializer(instance.product).data

        if instance.size_category:
            data["size_category"] = SizeCategorySerializer(instance.size_category).data

        if instance.category:
            data["category"] = CategorySerializer(instance.category).data

        if instance.vendor:
            data["vendor"] = SimpleVendorSerializer(instance.vendor).data

        return data

    def create(self, validated_data):
        validated_data["business"] = self.context["request"].user.business
        validated_data["category"] = validated_data["product"].category
        return super().create(validated_data)
