from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Task, Tile
from ..factories import TileFactory, TaskFactory
from tasks.api.serializers import TaskSerializer, TileSerializer, UserSerializer





class TaskViewsTest(APITestCase):
	@classmethod
	def setUpTestData(cls): #setup global data once for test suite

		TaskFactory.reset_sequence() #reset global sequence counter
		cls.tasks = TaskFactory.create_batch(3)
		cls.task = cls.tasks[0]

		cls.tile = Tile.objects.create(status="live", launch_date=timezone.now())
		cls.tile_serializer = TileSerializer(cls.tile)

	
	def test_str_representation(self):
		task_1 =  self.tasks[0]
		task_2 =  self.tasks[2]

		self.assertEqual(str(task_1), f"0. {task_1.title}")
		self.assertEqual(str(task_2), f"2. {task_2.title}")


	def test_can_browse_all_tasks(self):
		'''
			Ensure we can get list of tasks
		'''
		response = self.client.get(reverse("tasks:task-list"))
		
		for task in self.tasks:
			self.assertIn(
				TaskSerializer(instance=task).data,
				response.data
			)

		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.assertEqual(len(self.tasks), len(response.data))


	def test_can_read_a_specific_task(self):
		response = self.client.get(reverse("tasks:task-detail", args=[self.task.id]))

		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.assertEqual(TaskSerializer(instance=self.task).data, response.data)


	def test_can_add_a_new_task(self):
		user = User.objects.create_user(username='test_user_6', password='test_password')
		user_serializer = UserSerializer(user)
		self.client.login(username=user.username, password='test_password')
		
		payload = {
			"title": "New Task",
			"task_type": "discussion",
			"assignee": user_serializer.data,
			"description": "New task long description...",
			"tile": self.tile_serializer.data["id"], # use created tile id
		}


		response = self.client.post(reverse("tasks:task-list"), payload, format='json')

		created_task = Task.objects.get(title=payload["title"])

		self.assertEqual(status.HTTP_201_CREATED, response.status_code)

		# assert returned data is same as posted data
		for key, value in payload.items():
			self.assertEqual(value, response.data[key])


	def test_can_edit_a_task(self):
		'''
			Ensure we can update task 
		'''

		user = User.objects.create_user(username='test_user_6', password='test_password')
		user_serializer = UserSerializer(user)
		self.client.login(username=user.username, password='test_password')		
		
		payload = {
			"title": "New Task 2",
			"task_type": "discussion",
			"assignee": user,
			"description": "New task long description...",
			"tile": self.tile
		}

		update_payload = {
			"task_type": "diary",
			"assignee": user_serializer.data
		}


		new_task = Task.objects.create(**payload)
		response = self.client.patch(
			reverse("tasks:task-detail", args=[new_task.id]), update_payload, format="json")

		new_task.refresh_from_db()

		self.assertEqual(status.HTTP_200_OK, response.status_code)

		for key, value in update_payload.items():
			self.assertEqual(value, response.data[key])