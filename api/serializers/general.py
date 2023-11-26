from rest_framework import serializers

from api.models import Category, SizeCategory

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]

    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)


class SizeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeCategory
        fields =  ["id", "name"]
    
    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)