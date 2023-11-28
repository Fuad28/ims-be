from rest_framework import serializers

from api.models import Vendor


class SimpleVendorSerializer(serializers.ModelSerializer):
    qdp_rating= serializers.FloatField(read_only= True)
    completed_orders= serializers.IntegerField(read_only= True)
    lead_time= serializers.IntegerField(read_only= True)
    class Meta:
        model = Vendor
        fields = ["id", "name", "email", "phone_no", "qdp_rating",
                "completed_orders", "lead_time"]


class VendorSerializer(SimpleVendorSerializer):

    class Meta(SimpleVendorSerializer.Meta):
        fields = SimpleVendorSerializer.Meta.fields + ["products"]

    
    def create(self, validated_data):
        validated_data["business"]= self.context["request"].user.business
        return super().create(validated_data)