from django.contrib.auth.models import User
from rest_framework import serializers



class UserMixin(object):
	def get_user(self, data):
		try: #check if username is valid
			user =  User.objects.get(username=data["username"])
			return user
		
		except User.DoesNotExist:
			raise serializers.ValidationError("username is not valid.")



class DebugDBMixin(object):
	def dispatch(self, *args, **kwargs):
		response = super().dispatch(*args, **kwargs)

		from django.db import connection
		print('## of Queries: {}'.format(len(connection.queries)))

		for  query in connection.queries:
			print(query['sql'])

		return response			