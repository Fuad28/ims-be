from rest_framework import serializers

from api.models import Sale, SaleItem
from api.serializers.product import ProductItemSerializer
from api.serializers.customer import CustomerSerializer

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["id", "sale", "product_item", "quantity", "unit_selling_price", "selling_price", "discount"]


    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)
    

    def to_representation(self, instance: SaleItem):
        data= super().to_representation(instance)
        data["product_item"]= ProductItemSerializer(instance.product_item).data

        return data
        

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["id", "customer", "description", "discount", "total_selling_price", "sale_items"]

    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)
    

    def to_representation(self, instance: Sale):
        data= super().to_representation(instance)

        if instance.customer:
            data["customer"]= CustomerSerializer(instance.customer).data

        if instance.sale_items.count():
            data["sale_items"]= SaleItemSerializer(instance.sale_items.all(), many= True).data

        
        return data