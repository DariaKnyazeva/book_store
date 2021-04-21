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
        price = mommy.make(Category, amount=1,
                           period_limit=10)

        today = timezone.now().date()

        # rented today
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price))
        self.assertEqual(1, rent.days_rented)
        # the minimum amount is 1 * 10 days
        self.assertEqual(10, rent.price_per_book)

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()
        self.assertEqual(2, rent.days_rented)
        self.assertEqual(10, rent.price_per_book)

        recipe = Recipe(self.customer)
        self.assertEqual(20.00, recipe.caclulate_price())

    def test_calculate_price_categories(self):
        """
        Make sure that the recipy inclused
        the amount of books and the amount of days
        for different categories
        """
        price_regular = mommy.make(Category, amount=1.5, name="Regular",
                                   period_limit=10)
        price_fiction = mommy.make(Category, amount=3, name="Fiction",
                                   period_limit=10)
        price_novel = mommy.make(Category, amount=1.5, name="Novel",
                                 period_limit=10)

        today = timezone.now().date()

        # rented today
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_regular))
        self.assertEqual(15, rent.price_per_book)

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_fiction))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()
        self.assertEqual(30, rent.price_per_book)

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_novel))
        rent.created = today - timedelta(days=1)
        rent.save()
        self.assertEqual(15, rent.price_per_book)

        recipe = Recipe(self.customer)
        # 1.5 + 2 * 3 + 2 * 1.5 = 60
        # 15 + 30 + 15 = 45
        self.assertEqual(60, recipe.caclulate_price())

    def test_calculate_price_hit_limit(self):
        """
        Make sure that the recipy inclused
        the amount of books and the amount of days
        for different categories
        """
        price_regular = mommy.make(Category, amount=1.5, name="Regular",
                                   period_limit=2,
                                   changed_amount=2.0)
        # rented for 11 days
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_regular))
        today = timezone.now().date()
        rent.created = today - timedelta(days=10)
        rent.save()
        # 1.5 * 2 + 2.0 * 9 = 21.0
        self.assertEqual(21, rent.price_per_book)

    def test_get_price(self):
        recipe = Recipe(self.customer)
        self.assertEqual("$ 0.00", recipe.get_price())
