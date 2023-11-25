from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import Vendor
from api.serializers.vendor import VendorSerializer

class VendorViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= VendorSerializer

    def get_queryset(self):
        return Vendor.objects.filter(business= self.request.user.business)
