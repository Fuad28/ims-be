from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import Order
from api.serializers.order import OrderSerializer

class OrderViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(business= self.request.user.business)
