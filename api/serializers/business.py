from rest_framework import serializers

from api.models import Business


class BusinessSerializer(serializers.ModelSerializer):
    qdp_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "website",
            "email",
            "qdp_rating",
            "is_visible_as_vendor",
        ]
