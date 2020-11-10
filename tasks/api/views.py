from rest_framework import generics
from rest_framework import viewsets

from rest_framework.decorators import action

from ..models import  Tile, Task
from .serializers import TileSerializer, TaskSerializer
from .mixins import DebugDBMixin



class TileViewSet(DebugDBMixin, viewsets.ReadOnlyModelViewSet):
	queryset = Tile.objects.prefetch_related('tasks__assignee')
	serializer_class = TileSerializer



class TaskViewSet(DebugDBMixin, viewsets.ModelViewSet):

	queryset = (
		Task.objects.select_related('assignee')
	)
	serializer_class = TaskSerializer