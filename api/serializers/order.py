from rest_framework import serializers

from api.models import Order, OrderItem
from api.serializers.product import ProductItemSerializer
from api.serializers.vendor import SimpleVendorSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_item= ProductItemSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product_item", "cost_price",
                "total_cost_price", "qty_ordered", "qty_delayed",
                "qty_defected", "qty_accepted"]

    
    def to_representation(self, instance: OrderItem):
        data=  super().to_representation(instance)

        if  instance.product_item:
            data["product_item"]= ProductItemSerializer(instance= instance.product_item).data

        return data
        
class OrderSerializer(serializers.ModelSerializer):
    order_items= OrderItemSerializer(read_only= True)

    class Meta:
        model = Order
        fields = ["id", "vendor", "placement_date", "expected_receipt_date",
                 "actual_receipt_date", "cost_price",  "discount", "order_items"]
        
    
    def to_representation(self, instance: Order):
        data=  super().to_representation(instance)

        if  instance.vendor:
            data["vendor"]= SimpleVendorSerializer(instance= instance.vendor).data

        return data
