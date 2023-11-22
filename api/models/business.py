from django.db import models

from api.models import TimeAndUUIDStampedBaseModel

class Business(TimeAndUUIDStampedBaseModel):

	name = models.CharField(max_length= 255)
	website = models.URLField(null= True, blank= True)
	email= models.EmailField()
	qdp_rating = models.FloatField(default= 0)
	is_visible_as_vendor= models.BooleanField(default= False)

	def __str__(self):
		return f"{self.id}-{self.name}-{self.qdp_rating}"