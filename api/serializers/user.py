from django.db import transaction
from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer, 
    UserCreateSerializer as BaseUserCreateSerializer,
    )

from api.models import User, Business, TeamInvitation
from api.serializers.business import BusinessSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    business_name= serializers.CharField(max_length= 255, required= False)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "password", "email", "full_name", "phone", "business_name"]


    @transaction.Atomic
    def create(self, validated_data):
        business_name= validated_data.pop("business_name")
    
        if business_name:
            validated_data["business"] = Business.objects.create(
                name= business_name, 
                email= validated_data["email"]
            )
        
        
        else:
            invited_user_qs= TeamInvitation.objects.filter(
                email= validated_data["email"], 
                is_registered= False)

            if invited_user_qs.exists():
                invited_user= invited_user_qs.first()
                validated_data["role"]= invited_user.role
                validated_data["business"]= invited_user.business
                invited_user.is_registered= True
                invited_user.save()
            
            else:
                raise serializers.ValidationError("""
                    You have not been invited to the platform.
                    Request a member of your team to add you or create a business account
                    """)
                
                
        return super().create(validated_data)


class UserRetrieveSerializer(BaseUserSerializer):
    business= BusinessSerializer()
    class Meta:
        model = User
        fields = ["id", "full_name", "phone", "email", "business","role"]


class SimpleUserRetrieveSerializer(BaseUserSerializer):
    business= BusinessSerializer(allow_null= True)
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "business", "role"]