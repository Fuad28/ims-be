from rest_framework import serializers

from api.models import Vendor


class SimpleVendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ["id", "name", "email", "phone_no", "qdp_rating"]


class VendorSerializer(SimpleVendorSerializer):

    class Meta(SimpleVendorSerializer.Meta):
        fields = SimpleVendorSerializer.Meta.fields + ["products"]