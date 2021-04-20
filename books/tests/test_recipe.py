from datetime import timedelta
from model_mommy import mommy
from django.utils import timezone

from django.test import TestCase
from django.contrib.auth import get_user_model

from books.models import Book, BookRent
from books.recipe import Recipe
from pricing.models import Category

User = get_user_model()


class TestBookRecipe(TestCase):
    def setUp(self):
        super().setUp()
        self.customer = mommy.make(User)

    def test_calculate_price(self):
        """
        Make sure that the recipy inclused the amount of books and the amount of days
        """
        price = mommy.make(Category, amount=1)

        today = timezone.now().date()

        # rented today
        BookRent.objects.create(customer=self.customer,
                                status=BookRent.Status.RENTED,
                                book=mommy.make(Book, category=price))

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()

        recipe = Recipe(self.customer)
        self.assertEqual(3.00, recipe.caclulate_price())

    def test_calculate_price_categories(self):
        """
        Make sure that the recipy inclused
        the amount of books and the amount of days
        """
        price_regular = mommy.make(Category, amount=1.5, name="Regular")
        price_fiction = mommy.make(Category, amount=3, name="Fiction")
        price_novel = mommy.make(Category, amount=1.5, name="Novel")

        today = timezone.now().date()

        # rented today
        BookRent.objects.create(customer=self.customer,
                                status=BookRent.Status.RENTED,
                                book=mommy.make(Book, category=price_regular))

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_fiction))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_novel))
        rent.created = today - timedelta(days=1)
        rent.save()

        recipe = Recipe(self.customer)
        # 1.5 + 2 * 3 + 2 * 1.5 = 10.5
        self.assertEqual(10.5, recipe.caclulate_price())

    def test_get_price(self):
        recipe = Recipe(self.customer)
        self.assertEqual("$ 0.00", recipe.get_price())
