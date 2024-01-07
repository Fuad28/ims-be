from rest_framework.response import Response
from rest_framework import status

from djoser.views import UserViewSet as DjoserUserViewset


class UserViewSet(DjoserUserViewset):
    def perform_update(self, serializer):
        super().perform_update(serializer)

    def create(self, request, *args, **kwargs):
        if "email" in request.data:
            request.data["email"] = request.data["email"].lower()
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
