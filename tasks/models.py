from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .fields import OrderField



class Tile(models.Model):
	STATUS_CHOICES = (
		('live', 'Live'),
		('pending', 'Pending'),
		('archived', 'Archived'),
	)
	
	status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	launch_date = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.id} {self.status}"


class Task(models.Model):
	TYPE_CHOICES = (
		('survey', 'Survey'),
		('discussion', 'Discussion'),
		('diary', 'Diary'),
	)

	title = models.CharField(max_length=250)
	description = models.TextField()
	task_type =  models.CharField(max_length=20, choices=TYPE_CHOICES, default='survey')
	assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE)
	tile = models.ForeignKey(Tile, related_name='tasks', on_delete=models.CASCADE)
	order = OrderField(blank=True, for_fields=['tile'])
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return  f'{self.order}. {self.title}'