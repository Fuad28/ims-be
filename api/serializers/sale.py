from django.db import transaction
from rest_framework import serializers

from api.models import Sale, SaleItem, ProductItem
from api.serializers.product import ProductItemSerializer
from api.serializers.customer import CustomerSerializer


class CreateSaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["id", "product_item", "quantity"]


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = [
            "id",
            "sale",
            "product_item",
            "quantity",
            "unit_selling_price",
            "selling_price",
            "discount",
        ]

    def create(self, validated_data):
        validated_data["business"] = self.context["request"].user.business
        return super().create(validated_data)

    def to_representation(self, instance: SaleItem):
        data = super().to_representation(instance)
        data["product_item"] = ProductItemSerializer(instance.product_item).data

        return data


class SaleSerializer(serializers.ModelSerializer):
    total_selling_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    sale_items = CreateSaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "customer",
            "description",
            "discount",
            "total_selling_price",
            "sale_items",
        ]

    def to_representation(self, instance: Sale):
        data = super().to_representation(instance)

        if instance.customer:
            data["customer"] = CustomerSerializer(instance.customer).data

        if instance.sale_items.count():
            data["sale_items"] = SaleItemSerializer(instance.sale_items, many=True).data

        return data

    def validate_sale_items(self, sale_items: list):
        if not len(sale_items):
            raise serializers.ValidationError(
                "order must contain at least one sale_item"
            )

        for sale_item in sale_items:
            product_item: ProductItem = sale_item["product_item"]
            quantity = sale_item["quantity"]

            if product_item.quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough quantity of {product_item.name} available"
                )

        return sale_items

    @transaction.atomic
    def create(self, validated_data):
        business = self.context["request"].user.business
        validated_data["business"] = business
        sale_items = validated_data.pop("sale_items")
        sale: Sale = super().create(validated_data)

        total_selling_price = 0
        new_sale_items = []
        for sale_item in sale_items:
            unit_selling_price = sale_item["product_item"].selling_price
            selling_price = unit_selling_price * sale_item["quantity"]

            sale_item = SaleItem(
                **{
                    **sale_item,
                    "sale": sale,
                    "business": business,
                    "unit_selling_price": unit_selling_price,
                    "selling_price": selling_price,
                }
            )

            new_sale_items.append(sale_item)
            total_selling_price += selling_price

        sale_items = SaleItem.objects.bulk_create(new_sale_items)
        sale.total_selling_price = total_selling_price
        sale.save()

        # update product_item quantity
        product_items = []
        for sale_item in sale_items:
            sale_item.product_item.quantity -= sale_item.quantity
            product_items.append(sale_item.product_item)

        ProductItem.objects.bulk_update(product_items, ["quantity"])

        return sale
