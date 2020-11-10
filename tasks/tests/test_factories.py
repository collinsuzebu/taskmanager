from django.test import TestCase
from ..factories import TaskFactory, TileFactory


class TaskTestCase(TestCase):
	def test_model(self):
		"""Should be able to instantiate and save the model."""
		self.obj = TaskFactory()
		self.assertTrue(self.obj.pk)


class TileTestCase(TestCase):
	def test_model(self):
		"""Should be able to instantiate and save the model."""
		self.obj = TileFactory()
		self.assertTrue(self.obj.pk)