from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from api.models import Order, OrderItem, Vendor
from api.serializers.product import ProductItemSerializer
from api.serializers.vendor import SimpleVendorSerializer


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_item", "qty_ordered"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product_item",
            "unit_cost_price",
            "cost_price",
            "qty_ordered",
            "qty_delayed",
            "qty_defected",
            "qty_accepted",
        ]

    def to_representation(self, instance: OrderItem):
        data = super().to_representation(instance)

        if instance.product_item:
            data["product_item"] = ProductItemSerializer(
                instance=instance.product_item
            ).data

        return data


class OrderSerializer(serializers.ModelSerializer):
    total_cost_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    order_items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "vendor",
            "placement_date",
            "status",
            "expected_receipt_date",
            "actual_receipt_date",
            "total_cost_price",
            "discount",
            "order_items",
        ]

    def to_representation(self, instance: Order):
        data = super().to_representation(instance)

        if instance.vendor:
            data["vendor"] = SimpleVendorSerializer(instance=instance.vendor).data

        if instance.order_items.count():
            data["order_items"] = OrderItemSerializer(
                instance=instance.order_items.all(), many=True
            ).data

        return data

    def validate_order_items(self, order_items: list):
        if not len(order_items):
            raise serializers.ValidationError(
                "order must contain at least one order_item"
            )

        return order_items

    @transaction.atomic
    def create(self, validated_data):
        business = self.context["request"].user.business
        validated_data["business"] = business
        order_items = validated_data.pop("order_items")
        order: Order = super().create(validated_data)

        total_cost_price = 0
        new_order_items = []
        for order_item in order_items:
            unit_cost_price = order_item["product_item"].cost_price
            cost_price = unit_cost_price * order_item["qty_ordered"]

            order_item = OrderItem(
                **{
                    **order_item,
                    "order": order,
                    "business": business,
                    "unit_cost_price": unit_cost_price,
                    "cost_price": cost_price,
                }
            )

            new_order_items.append(order_item)
            total_cost_price += cost_price

        OrderItem.objects.bulk_create(new_order_items)
        order.total_cost_price = total_cost_price
        order.save()

        return order


class OrderReceiptProcessingSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all())
    status = serializers.CharField(max_length=30, required=False)
    qty_delayed = serializers.IntegerField()
    qty_defected = serializers.IntegerField()
    qty_accepted = serializers.IntegerField()

    def validate_id(self, order_item: OrderItem):
        order: Order = self.context["order"]

        if not order.order_items.filter(id=order_item.id).exists():
            raise serializers.ValidationError("Invalid order_item id")

        return order_item

    def validate(self, attrs):
        order_item: OrderItem = attrs["id"]
        qty_delayed = attrs["qty_delayed"]
        qty_defected = attrs["qty_defected"]
        qty_accepted = attrs["qty_accepted"]
        total_qty = qty_delayed + qty_defected + qty_accepted

        if total_qty != order_item.qty_ordered:
            raise serializers.ValidationError("All order items must be accounted for.")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        order: Order = self.context["order"]
        vendor: Vendor = order.vendor
        order_item: OrderItem = validated_data["id"]
        qty_delayed = validated_data["qty_delayed"]
        qty_defected = validated_data["qty_defected"]
        qty_accepted = validated_data["qty_accepted"]

        order_item.product_item.quantity += qty_accepted
        order_item.product_item.save()

        order_item.qty_accepted = qty_accepted
        order_item.qty_delayed = qty_delayed
        order_item.qty_defected = qty_defected
        order_item.save()

        order.actual_receipt_date = timezone.now().date()
        if validated_data["status"]: order.status = validated_data["status"]
        order.save()

        vendor.completed_orders += 1
        vendor.total_lead_time += (
            order.actual_receipt_date - order.placement_date
        ).days
        vendor.total_qdp_rating += order.compute_qdp()
        vendor.lead_time = vendor.avg_lead_time
        vendor.qdp_rating += vendor.avg_qdp_rating
        vendor.save()
