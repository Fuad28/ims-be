from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import Sale
from api.serializers.sale import SaleSerializer

class SaleViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= SaleSerializer

    def get_queryset(self):
        return Sale.objects.filter(business= self.request.user.business)
