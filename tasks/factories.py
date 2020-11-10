import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import factory.django
import factory.fuzzy
from .models import Tile, Task


class UserFactory(factory.django.DjangoModelFactory):
	username = factory.Sequence(lambda n: 'username_{}'.format(n))

	class Meta:
		model = User


class TileFactory(factory.django.DjangoModelFactory):
	status = "pending"
	launch_date = factory.LazyFunction(timezone.now)

	class Meta:
		model = Tile


class TaskFactory(factory.django.DjangoModelFactory):
	title = factory.Faker("word")
	description = factory.Faker("text")
	task_type =  "survey"
	order = factory.Sequence(lambda n: n)
	assignee = factory.SubFactory(UserFactory)
	tile = factory.SubFactory(TileFactory)
	created = factory.LazyFunction(timezone.now)
	updated = factory.LazyFunction(timezone.now)

	class Meta:
		model = Task