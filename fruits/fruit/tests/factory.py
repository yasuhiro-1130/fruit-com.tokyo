import factory
from ..models import *
import random
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
	email = 'test_factory@test.com'
	name = 'test_user'
	password = 'test'
	is_staff = False
	is_active = True
	date_joined = timezone.now()

	class Meta:
		model = User


class FarmFactory(factory.django.DjangoModelFactory):
	farm_name = "test農園"
	user = factory.SubFactory(UserFactory)

	class Meta:
		model = Farm


class FarmProductFactory(factory.django.DjangoModelFactory):
	product_name = '美味しいりんご'
	product_category = 'りんご'
	product_origin = '青森県産'
	product_description = '美味しい'
	product_weight = '10'
	product_stock = '5'
	product_price = '5000'
	created = timezone.now()
	updated = timezone.now()
	available = True
	farm = factory.SubFactory(FarmFactory)

	class Meta:
		model = FarmProduct


class ShoppingCartFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)

	class Meta:
		model = ShoppingCart


class ShoppingCartItemFactory(factory.django.DjangoModelFactory):
	cart = factory.SubFactory(ShoppingCartFactory)
	product = factory.SubFactory(FarmProductFactory)
	amount = '7'

	class Meta:
		model = ShoppingCartItem


class ReviewFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)
	product = factory.SubFactory(FarmProductFactory)
	rating = '3'
	comment = 'とても美味しかったです'
	created = timezone.now()
	updated = timezone.now()

	class Meta:
		model = Review


class OrderFactory(factory.django.DjangoModelFactory):
	user = factory.SubFactory(UserFactory)
	is_shipped = False
	is_settled = False
	stripe_id = 'dafadl;k]as;:df]ga@d:lg][adgre43]'
	created_at = timezone.now()

	class Meta:
		model = Order


class OrderedItemFactory(factory.django.DjangoModelFactory):
	order = factory.SubFactory(OrderFactory)
	product = factory.SubFactory(FarmProductFactory)
	amount = '9'

	class Meta:
		model = OrderedItem





