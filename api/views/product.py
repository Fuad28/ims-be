from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import Product, ProductItem, ProductCategory, ProductSizeCategory
from api.serializers.product import (
    ProductSerializer, 
    ProductItemSerializer, 
    ProductCategorySerializer,
    ProductSizeCategorySerializer)


class ProductViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(business= self.request.user.business)


class ProductItemViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= ProductItemSerializer

    def get_queryset(self):
        return ProductItem.objects.filter(business= self.request.user.business)


class ProductCategoryViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= ProductCategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.filter(business= self.request.user.business)



class ProductSizeCategoryViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class= ProductSizeCategorySerializer

    def get_queryset(self):
        return ProductSizeCategory.objects.filter(business= self.request.user.business)