from rest_framework import serializers

from api.models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["id", "name", "email"]

    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)