from rest_framework import generics
from rest_framework import viewsets

from rest_framework.decorators import action

from ..models import  Tile, Task
from .serializers import TileSerializer, TaskSerializer
from .mixins import DebugDBMixin



class TileViewSet(viewsets.ModelViewSet):
	queryset = Tile.objects.all()
	serializer_class = TileSerializer



	# @action(detail=True, methods=['get'], serializer_class=TileSerializerWithTasks)
	# def tasks(self, request, *args, **kwargs):
	# 	return self.retrieve(request, *args, **kwargs)


# ReadOnlyModelViewSet
class TaskViewSet(viewsets.ModelViewSet):

	queryset = (
		Task.objects.select_related('tile',)
	)
	serializer_class = TaskSerializer