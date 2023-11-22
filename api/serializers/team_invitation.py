from rest_framework import serializers

from api.enums import UserRoleEnum

class TeamInvitationDataSerializer(serializers.Serializer):
	email = serializers.EmailField()
	role = serializers.CharField(max_length= 11)
	
	def validate(self, attrs):
		if attrs["role"] not in UserRoleEnum.values:
			raise serializers.ValidationError(f"role can only be one of {UserRoleEnum.values}")

class TeamInvitationSerializer(serializers.Serializer):
	data = serializers.ListField(child= TeamInvitationDataSerializer(), allow_empty= False)