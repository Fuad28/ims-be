from rest_framework import serializers

from api.models import Order, OrderItem
from api.serializers.product import ProductItemSerializer
from api.serializers.vendor import SimpleVendorSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_item= ProductItemSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product_item", "cost_price", "quantity", "total_cost_price"]
        
class OrderSerializer(serializers.ModelSerializer):
    vendor= SimpleVendorSerializer()
    order_items= OrderItemSerializer()

    class Meta:
        model = Order
        fields = ["id", "vendor", "placement_date",
                "expected_receipt_date", "actual_receipt_date", "cost_price",
                "discount", "qty_delayed", "qty_defected", "qty_accepted", "order_items"]