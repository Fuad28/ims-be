from django.db import models

from api.models import TimeAndUUIDStampedBaseModel, Business

class TeamInvitation(TimeAndUUIDStampedBaseModel):
	
	email = models.EmailField(unique= True)
	business= models.ForeignKey(Business, related_name= "invitations", on_delete= models.CASCADE)
	is_registered= models.BooleanField(default= False)

	def __str__(self):
		return f"{self.id}-{self.email}-{self.business.id}-{self.is_registered}"

