from datetime import timedelta
from model_mommy import mommy
from django.utils import timezone

from django.test import TestCase
from django.contrib.auth import get_user_model

from books.models import Book, BookRent
from books.recipe import Recipe
from pricing.models import Price

User = get_user_model()


class TestBookRecipe(TestCase):
    def setUp(self):
        super().setUp()
        self.customer = mommy.make(User)

    def test_calculate_price(self):
        """
        Make sure that the recipy inclused the amount of books and the amount of days
        """
        price = mommy.make(Price, amount=1)

        today = timezone.now().date()

        # rented today
        BookRent.objects.create(customer=self.customer,
                                price=price,
                                status=BookRent.Status.RENTED,
                                book=mommy.make(Book))

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       price=price,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()

        recipe = Recipe(self.customer)
        self.assertEqual(3.00, recipe.caclulate_price())

    def test_get_price(self):
        recipe = Recipe(self.customer)
        self.assertEqual("$ 0.00", recipe.get_price())
