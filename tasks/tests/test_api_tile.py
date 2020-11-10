from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Task, Tile
from ..factories import TileFactory, TaskFactory
from tasks.api.serializers import TaskSerializer, TileSerializer, UserSerializer



class TileViewsTest(APITestCase):
	"""
		Test Tile related views
	"""

	@classmethod
	def setUpTestData(cls):

		TileFactory.reset_sequence()
		cls.tiles = TileFactory.create_batch(3)
		cls.tile = cls.tiles[0]


	def test_can_browse_all_tiles(self):
		'''
			Ensure we can get list of tiles
		'''
		response = self.client.get(reverse("tasks:tile-list"))

		for tile in self.tiles:
			self.assertIn(
				TileSerializer(instance=tile).data,
				response.data)


		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.assertEqual(len(self.tiles), len(response.data))

	
	def test_can_read_a_specific_tile(self):
		response = self.client.get(reverse("tasks:tile-detail", args=[self.tile.id]))

		self.assertEqual(status.HTTP_200_OK, response.status_code)
		self.assertEqual(TileSerializer(instance=self.tile).data, response.data)