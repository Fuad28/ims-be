from django.urls import path
from rest_framework_nested import routers
from rest_framework_simplejwt import views as simple_jwt_views


from api.views import (
    UserViewSet,
    TeamInvitationView,
)


app_name = "api"

urlpatterns = [
    #onboarding
    path("login/", simple_jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("refresh/", simple_jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path("verify/", simple_jwt_views.TokenVerifyView.as_view(), name="verify-token"),
    path("users/", UserViewSet.as_view({"post": "create"}), name="users"),
    path("me/", UserViewSet.as_view({"get": "me", "delete": "me", "patch": "me", "put": "me"})),
    path("invite-team/", TeamInvitationView.as_view(), name="invite-team"),


    
    ] # + router.urls
