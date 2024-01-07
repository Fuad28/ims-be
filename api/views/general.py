from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import SizeCategory, Category
from api.serializers.general import SizeCategorySerializer, CategorySerializer


class SizeCategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SizeCategorySerializer

    def get_queryset(self):
        return SizeCategory.objects.filter(business=self.request.user.business)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(business=self.request.user.business)
