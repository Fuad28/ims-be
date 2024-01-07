from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.models import Order
from api.serializers.order import OrderSerializer, OrderReceiptProcessingSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(business=self.request.user.business)

    @action(detail=True, methods=["patch"], url_path="order-reciept-processing")
    def order_reciept_processing(self, request, pk):
        order: Order = self.get_object()

        serializer = OrderReceiptProcessingSerializer(
            data=request.data, many=True, context={"order": order}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "processed"}, status=status.HTTP_200_OK)
