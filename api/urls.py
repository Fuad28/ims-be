from django.urls import path
from rest_framework_nested import routers
from rest_framework_simplejwt import views as simple_jwt_views


from api.views import (
    UserViewSet,
    TeamInvitationView,
    CustomerViewSet,
    OrderViewSet,
    ProductViewSet,
    ProductItemViewSet,
    ProductCategoryViewSet,
    ProductSizeCategoryViewSet,
    SaleViewSet,
    VendorViewSet

)

app_name = "api"

router = routers.DefaultRouter()
router.register("customers", CustomerViewSet, basename= "customer-view")
router.register("orders", OrderViewSet, basename= "order-view")
router.register("products", ProductViewSet, basename= "product-view")
router.register("product-items", ProductItemViewSet, basename= "product-view")
router.register("product-categories", ProductCategoryViewSet, basename= "product-category-view")
router.register("product-size-categories-items", ProductSizeCategoryViewSet, basename= "product-size-category-view")
router.register("sales", SaleViewSet, basename= "sale-view")
router.register("vendors", VendorViewSet, basename= "vendor-view")


urlpatterns = [
    #onboarding
    path("login/", simple_jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("refresh/", simple_jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path("verify/", simple_jwt_views.TokenVerifyView.as_view(), name="verify-token"),
    path("sign-up/", UserViewSet.as_view({"post": "create"}), name="users"),
    path("me/", UserViewSet.as_view({"get": "me", "delete": "me", "patch": "me", "put": "me"})),
    path("invite-team/", TeamInvitationView.as_view(), name="invite-team"),


    
    ]  + router.urls
