from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Tile, Task
from .mixins import UserMixin, DebugDBMixin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        extra_kwargs = {
            'username': {'validators': []},
            'email': {'read_only':True}
        }



class TaskSerializer(UserMixin, serializers.ModelSerializer):
	assignee = UserSerializer()
	
	class Meta:
		model = Task
		fields = ['id', 'tile', 'title', 'task_type', 'assignee', 'description', 'created']
		# read_only_fields = ['tile']

	def create(self, validated_data):
		assignee_data = validated_data.pop('assignee')
		# check assigned user is valid or raise validation error
		validated_data["assignee"] = self.get_user(assignee_data)
		task = self.Meta.model.objects.create(**validated_data)
		return task


	def update(self, instance, validated_data):
		assignee_data = validated_data.get('assignee')

		# TODO - create partial update serialier with custom logic
		if assignee_data:
			instance.assignee = self.get_user(assignee_data)		

		# get updated fields values or use existing values
		for key in validated_data:
			if key != "assignee":
				setattr(
					instance, 
					key, 
					validated_data.get(key, getattr(instance, key))
				)
		instance.save()
		return instance




class TileSerializer(UserMixin, serializers.ModelSerializer):
	tasks = TaskSerializer(many=True)
	class Meta:
		model = Tile
		fields = ['id', 'status', 'launch_date', 'tasks', ]