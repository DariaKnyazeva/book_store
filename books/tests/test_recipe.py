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

        today = timezone.now().date()

        price_regular = mommy.make(Category, amount=1.5, name="Regular",
                                   period_limit=10,
                                   currency=self.currency)
        price_fiction = mommy.make(Category, amount=3, name="Fiction",
                                   period_limit=10,
                                   currency=self.currency)
        price_novel = mommy.make(Category, amount=1.5, name="Novel",
                                 period_limit=10,
                                 currency=self.currency)

        self.today_regular_rent = BookRent.objects.create(customer=self.customer,
                                                          status=BookRent.Status.RENTED,
                                                          book=mommy.make(Book, category=price_regular))
        self.yesterday_fiction_rent = BookRent.objects.create(customer=self.customer,
                                                              status=BookRent.Status.RENTED,
                                                              book=mommy.make(Book, category=price_fiction))
        self.yesterday_fiction_rent.created = today - timedelta(days=1)
        self.yesterday_fiction_rent.save()
        self.yesterday_novel_rent = BookRent.objects.create(customer=self.customer,
                                                            status=BookRent.Status.RENTED,
                                                            book=mommy.make(Book, category=price_novel))
        self.yesterday_novel_rent.created = today - timedelta(days=1)
        self.yesterday_novel_rent.save()

    def test_days_rented(self):
        self.assertEqual(1, self.today_regular_rent.days_rented)
        self.assertEqual(2, self.yesterday_fiction_rent.days_rented)

    def test_price_regular(self):
        """
        Make sure that the recipy inclused
        the amount of books and the amount of days
        for different categories
        """
        charge = self.today_regular_rent.price_and_details
        self.assertEqual(15, charge[0])
        self.assertEqual("Rented for 1 days: $ 15.0 minimum charge", charge[1])

    def test_price_fiction(self):
        charge = self.yesterday_fiction_rent.price_and_details
        self.assertEqual(30, charge[0])
        self.assertEqual("Rented for 2 days: $ 30 minimum charge", charge[1])

    def test_price_novel(self):
        charge = self.yesterday_novel_rent.price_and_details
        self.assertEqual(15, charge[0])
        self.assertEqual("Rented for 2 days: $ 15.0 minimum charge", charge[1])
        self.assertEqual(f"{self.yesterday_novel_rent.book.title} (Novel): {charge[1]}",
                         str(self.yesterday_novel_rent))

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
        charge = rent.price_and_details
        self.assertEqual(21, charge[0])
        self.assertEqual("Rented for 11 days: $ 1.5 for 2 + $ 2.0 for 9 days", charge[1])

    def test_get_price_repr(self):
        recipe = Recipe(self.customer)
        # sum of all of the customer's rents
        self.assertEqual("$ 60.00", recipe.get_price_repr())
