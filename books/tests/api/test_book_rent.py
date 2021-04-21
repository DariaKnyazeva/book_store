import json
from model_mommy import mommy

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookRent
from pricing.models import Category, Currency

User = get_user_model()


class TestBookRentApi(TestCase):
    def setUp(self):
        self.api_url = reverse("books-api:book-rents")

    def login_user(self):
        password = "test"
        self.user, _ = User.objects.get_or_create(is_active=True, username="test", user_role=1, password=password)
        self.user.set_password(password)
        self.user.save()

        lg = self.client.login(username=self.user.username, password=password)
        self.assertTrue(lg)

    def test_book_rents_empty_list(self):
        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        self.assertListEqual([], json.loads(response.content)['results'])

    def test_book_rents_other_user(self):
        """
        Make sure that if user is not logged in, other's rents are not returned
        """
        currency = Currency.get_default_currency()

        category = mommy.make(Category, name="Regular", currency=currency)
        book1 = mommy.make(Book, title="Abc", category=category)
        book2 = mommy.make(Book, title="Xyz", category=category)

        user = mommy.make(User)
        mommy.make(BookRent, book=book1, customer=user)
        mommy.make(BookRent, book=book2, customer=user)

        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)['results']
        self.assertListEqual([], content)

        user_url = "http://testserver" + reverse("users-api:user", kwargs={"pk": user.id})

        for rent_detail in content:
            self.assertEqual(user_url, rent_detail['customer'])

    def test_book_rents(self):
        """
        Make sure that if user is not logged in, other's rents are not returned
        """
        currency = Currency.get_default_currency()

        category = mommy.make(Category, name="Regular", currency=currency)
        book1 = mommy.make(Book, title="Abc", category=category)
        book2 = mommy.make(Book, title="Xyz", category=category)

        self.login_user()

        my_rent = mommy.make(BookRent, book=book1, customer=self.user)
        mommy.make(BookRent, book=book2)

        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)['results']
        self.assertEqual(1, len(content))

        book_url = "http://testserver" + reverse("books-api:book", kwargs={"pk": book1.id})

        self.assertEqual(book_url, content[0]['book'])
        self.assertEqual(my_rent.id, content[0]['id'])

    def test_book_rent_create(self):
        currency = Currency.get_default_currency()
        category = mommy.make(Category, name="Regular", currency=currency)

        book = mommy.make(Book, title="Abc", category=category)

        rent_count = BookRent.objects.count()

        book_url = "http://testserver" + reverse("books-api:book", kwargs={"pk": book.id})

        data = {
            'book': book_url,
        }

        self.login_user()

        response = self.client.post(self.api_url, data=data, format='json')
        self.assertEqual(201, response.status_code)
        content = json.loads(response.content)
        self.assertEqual(rent_count + 1, BookRent.objects.count())
        new_rent = BookRent.objects.get(id=content['id'])
        self.assertEqual(self.user, new_rent.customer)
