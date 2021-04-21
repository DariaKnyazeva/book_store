import json
from model_mommy import mommy

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from books.models import Book
from pricing.models import Category

User = get_user_model()


class TestBookApi(TestCase):
    def setUp(self):
        self.api_url = reverse("books-api:books")

    def test_books_empty_list(self):
        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        self.assertListEqual([], json.loads(response.content)['results'])

    def test_books(self):
        category = mommy.make(Category, name="Regular")
        book1 = mommy.make(Book, title="Abc", category=category)
        book2 = mommy.make(Book, title="Xyz", category=category)

        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)['results']
        self.assertEqual(2, len(content))

        category_url = "http://testserver" + reverse("pricing-api:category", kwargs={"pk": category.id})

        expected = [
            {'id': book1.id, 'title': 'Abc', 'category': category_url},
            {'id': book2.id, 'title': 'Xyz', 'category': category_url}
        ]
        self.assertListEqual(expected, content)

    def test_book_create(self):
        category = mommy.make(Category, name="Regular")

        book_count = Book.objects.count()

        category_url = "http://testserver" + reverse("pricing-api:category", kwargs={"pk": category.id})

        data = {
            'title': 'Test Title',
            'category': category_url,
        }

        response = self.client.post(self.api_url, data=data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(book_count + 1, Book.objects.count())
