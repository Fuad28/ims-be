from django.db import models

import uuid


from api.models import TimeAndUUIDStampedBaseModel
class Business(models.Model):

	id = models. UUIDField(default=uuid.uuid4, editable=False, primary_key= True)
	name = models.CharField(max_length= 255)
	website = models.URLField(null= True, blank= True)
	email= models.EmailField()
	qdp_rating = models.FloatField(default= 0)
	is_visible_as_vendor= models.BooleanField(default= False)
	created_at = models.DateTimeField(auto_now= True)
	updated_at = models.DateTimeField(auto_now_add= True)


	def __str__(self):
		return f"{self.id}-{self.name}-{self.qdp_rating}"
	

class BusinessTimeAndUUIDStampedBaseModel(TimeAndUUIDStampedBaseModel):
	"""
	Base model class that contains special fields other model classes will subclass from.
	It inherits from TimeAndUUIDStampedBaseModel.

	Fields:
	business (Business): business the record belongs to.
	
	"""

	business = models.ForeignKey(Business, on_delete= models.CASCADE, related_name= '%(class)s')
	class Meta:
		abstract = True