from datetime import timedelta
from model_mommy import mommy
from django.utils import timezone

from django.test import TestCase
from django.contrib.auth import get_user_model

from books.models import Book, BookRent
from books.recipe import Recipe
from pricing.models import Category, Currency

User = get_user_model()


class TestBookRecipe(TestCase):
    def setUp(self):
        super().setUp()
        self.customer = mommy.make(User)
        self.currency = mommy.make(Currency, symbol="$")

    def test_calculate_price(self):
        """
        Make sure that the recipy inclused the amount of books and the amount of days
        """
        price = mommy.make(Category, amount=1,
                           period_limit=10,
                           currency=self.currency)

        today = timezone.now().date()

        # rented today
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price))
        self.assertEqual(1, rent.days_rented)
        # the minimum amount is 1 * 10 days
        charge = rent.price_per_book
        self.assertEqual(10, charge[0])
        self.assertEqual("Rented for 1 days: $ 10 minimum charge", charge[1])

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()
        self.assertEqual(2, rent.days_rented)
        charge = rent.price_per_book
        self.assertEqual(10, charge[0])
        self.assertEqual("Rented for 2 days: $ 10 minimum charge", charge[1])

        recipe = Recipe(self.customer)
        self.assertEqual(20.00, recipe.caclulate_price())

    def test_calculate_price_categories(self):
        """
        Make sure that the recipy inclused
        the amount of books and the amount of days
        for different categories
        """
        price_regular = mommy.make(Category, amount=1.5, name="Regular",
                                   period_limit=10,
                                   currency=self.currency)
        price_fiction = mommy.make(Category, amount=3, name="Fiction",
                                   period_limit=10,
                                   currency=self.currency)
        price_novel = mommy.make(Category, amount=1.5, name="Novel",
                                 period_limit=10,
                                 currency=self.currency)

        today = timezone.now().date()

        # rented today
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_regular))
        charge = rent.price_per_book
        self.assertEqual(15, charge[0])
        self.assertEqual("Rented for 1 days: $ 15.0 minimum charge", charge[1])

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_fiction))
        # Have to set up created because it is auto set to today on creation
        rent.created = today - timedelta(days=1)
        rent.save()
        charge = rent.price_per_book
        self.assertEqual(30, charge[0])
        self.assertEqual("Rented for 2 days: $ 30 minimum charge", charge[1])

        # rented yesterday
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_novel, title="A"))
        rent.created = today - timedelta(days=1)
        rent.save()
        charge = rent.price_per_book
        self.assertEqual(15, charge[0])
        self.assertEqual("Rented for 2 days: $ 15.0 minimum charge", charge[1])
        self.assertEqual(f"{rent.book.title} (Novel): {charge[1]}", str(rent))

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
                                   changed_amount=2.0,
                                   currency=self.currency)
        # rented for 11 days
        rent = BookRent.objects.create(customer=self.customer,
                                       status=BookRent.Status.RENTED,
                                       book=mommy.make(Book, category=price_regular))
        today = timezone.now().date()
        rent.created = today - timedelta(days=10)
        rent.save()
        # 1.5 * 2 + 2.0 * 9 = 21.0
        charge = rent.price_per_book
        self.assertEqual(21, charge[0])
        self.assertEqual("Rented for 11 days: $ 1.5 for 2 + $ 2.0 for 9 days", charge[1])

    def test_get_price(self):
        recipe = Recipe(self.customer)
        self.assertEqual("$ 0.00", recipe.get_price())
