from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Task, Tile
from ..factories import TaskFactory, TileFactory


class TileModelTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		TileFactory.reset_sequence() #reset global sequence counter
		cls.tile = TileFactory()


	def test_it_has_required_fields(self):
		self.assertIsInstance(self.tile.status, str)
		self.assertIsInstance(self.tile.launch_date, datetime)


	def test_it_has_auto_generated_fields(self):
		self.assertIsInstance(self.tile.created, datetime)


	def test_it_can_have_multiple_tasks(self):
		tasks = TaskFactory.create_batch(3)

		for task in tasks:
			self.tile.tasks.add(task)

		for task in tasks:
			self.assertIn(task, self.tile.tasks.all())

		self.assertEquals(len(tasks), self.tile.tasks.count())

	def test_str_representation_is_status(self):
		self.assertEqual(str(self.tile), f"1 pending")




class TaskModelTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		TaskFactory.reset_sequence() #reset global sequence counter
		cls.tasks = TaskFactory.create_batch(3)
		cls.task = cls.tasks[0]


	def test_it_has_required_fields(self):
		self.assertIsInstance(self.task.title, str)
		self.assertIsInstance(self.task.description, str)
		self.assertIsInstance(self.task.task_type, str)
		self.assertIsInstance(self.task.assignee, User)


	def test_it_has_auto_generated_fields(self):
		self.assertIsInstance(self.task.tile, Tile)
		self.assertIsInstance(self.task.order, int)
		self.assertIsInstance(self.task.created, datetime)
		self.assertIsInstance(self.task.updated, datetime)


	def test_str_representation_is_title(self):
		self.assertEqual(str(self.task), f"0. {self.task.title}")