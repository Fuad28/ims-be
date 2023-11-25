from rest_framework import serializers

from api.models import Product, ProductCategory, ProductItem, ProductSizeCategory
from api.serializers.vendor import SimpleVendorSerializer

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "image", "quantity"]


    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)



class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "product"]

    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)
    

    def to_representation(self, instance: ProductCategory):
        data=  super().to_representation(instance)
        data["product"]= ProductSerializer(instance= instance.product).data

        return data



class ProductSizeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeCategory
        fields =  ["id", "name", "product"]

    
    def to_representation(self, instance: ProductSizeCategory):
        data=  super().to_representation(instance)
        data["product"]= ProductSerializer(instance= instance.product).data

        return data
    
    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)


class ProductItemSerializer(serializers.ModelSerializer):
    serial_no= serializers.CharField(max_length= 10, read_only= True)

    class Meta:
        model = ProductItem
        fields = [
            "id", "serial_no", "quantity", "safety_stock", "reordering_point",
            "cost_price", "selling_price", "holding_cost", 
            "ordering_cost", "expiring_date", "barcode", "image",
            "product", "size_category", "category", "vendor"
        ]

    def to_representation(self, instance: ProductItem):
        data=  super().to_representation(instance)

        if instance.product:
            data["product"]= ProductSerializer(instance.product).data

        if instance.size_category:
            data["size_category"]= ProductCategorySerializer(instance.size_category).data

        if instance.category:
            data["category"]= ProductCategorySerializer(instance.category).data

        
        if instance.vendor:
            data["vendor"]= SimpleVendorSerializer(instance.vendor).data

        return data
    

    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)