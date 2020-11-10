from django.urls import path, include

from rest_framework import routers

from . import views


app_name = 'tasks'

router = routers.DefaultRouter()
router.register('tasks', views.TaskViewSet)
router.register('tiles', views.TileViewSet)



urlpatterns = [
	path('', include(router.urls)),
]