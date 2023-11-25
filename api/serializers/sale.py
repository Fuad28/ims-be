from rest_framework import serializers

from api.models import Sale, SaleItem
from api.serializers.product import ProductItemSerializer
from api.serializers.customer import CustomerSerializer

class SaleItemSerializer(serializers.ModelSerializer):
    product_item= ProductItemSerializer()

    class Meta:
        model = SaleItem
        fields = ["id", "sale", "product_item", "quantity", "cost_price", "discount"]
        

class SaleSerializer(serializers.ModelSerializer):
    customer= CustomerSerializer()

    class Meta:
        model = Sale
        fields = ["id", "customer", "discount", "total_cost"]