from rest_framework import serializers

from api.models import Order
from api.serializers.product import ProductItemSerializer
from api.serializers.vendor import SimpleVendorSerializer

class OrderSerializer(serializers.ModelSerializer):
    product_item= ProductItemSerializer()
    vendor= SimpleVendorSerializer()

    class Meta:
        model = Order
        fields = ["id", "product_item", "vendor", "placement_date",
                "expected_receipt_date", "actual_receipt_date", "cost_price",
                "discount", "qty_delayed", "qty_defected", "qty_accepted"]