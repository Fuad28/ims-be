from django.db import models

from api.models import TimeAndUUIDStampedBaseModel, Business
from api.enums import UserRoleEnum
class TeamInvitation(TimeAndUUIDStampedBaseModel):
	
	email = models.EmailField(unique= True)
	business= models.ForeignKey(Business, related_name= "invitations", on_delete= models.CASCADE)
	role =  models.CharField(max_length= 11, choices= UserRoleEnum.choices, default= UserRoleEnum.STORE_CLERK)
	is_registered= models.BooleanField(default= False)

	def __str__(self):
		return f"{self.id}-{self.email}-{self.business.id}-{self.is_registered}"

