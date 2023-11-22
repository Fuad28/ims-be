from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet 

import uuid


class SoftDeletionQuerySet(QuerySet):
	def delete(self, hard=False):
		if hard:
			return super(SoftDeletionQuerySet, self).delete() 
		return super (SoftDeletionQuerySet, self) .update(deleted_at=timezone.now())
	
	def alive(self):
		return self.filter(deleted_at=None)
	
	def dead(self):
		return self.exclude(deleted_at=None)
	

class SoftDeletionManager(models.Manager) :
	def get_queryset(self) :
		return SoftDeletionQuerySet(self.model).filter(deleted_at__isnull=True)


class TimeAndUUIDStampedBaseModel(models.Model):
	"""Base model class that contains special fields other model classes will subclass from
	Fields:
	created_at (DateTime): Time at which the object was created 
	updated_at (Datetime): Time at which the object was updated 
	id (String): UUID representing ID of each model"""

	id = models. UUIDField(default=uuid.uuid4, editable=False, primary_key= True)

	created_at = models.DateTimeField(auto_now= True)
	updated_at = models.DateTimeField(auto_now_add= True)

	class Meta:
		abstract = True


class SoftDeleteBaseModel(models.Model):
	"""
	Base model class that implements soft deletion for other models that will subclass from it
	Fields:
	deleted_at (DateTime): Time at which action to delete an object was taken
	"""
	deleted_at = models.DateTimeField (blank=True, null=True)
	objects = SoftDeletionManager()
	all_objects = models.Manager() 
	
	class Meta:
		abstract = True

	def delete(self, hard=True) :
		if hard:
			super(SoftDeleteBaseModel, self).delete()
		else:
			super(SoftDeleteBaseModel, self).delete()
			self.deleted_at = timezone.now()
			self.save()
	
	def restore (self):
		self.deleted_at = None
		self.save()