from model_mommy import mommy

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from books.models import Book


class TestBookListView(TestCase):
    def test_list_no_books(self):
        url = reverse('books:book-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTrue("No books found" in str(response.content))

    def test_list_few_books(self):
        for _i in range(3):
            mommy.make(Book)

        url = reverse('books:book-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertFalse("No books found" in str(response.content))
        self.assertTrue(Book.objects.all()[0].title in str(response.content))

    def test_pagination(self):
        for i in range(1, 100):
            mommy.make(Book, title=f"Book {i}")

        num_page = 2
        url = reverse('books:book-list') + f'?page={num_page}'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertFalse("No books found" in str(response.content))
        self.assertFalse("Book 0" in str(response.content))
        self.assertTrue("Book 24" in str(response.content))

    def test_search(self):
        mommy.make(Book, title="Alice")
        mommy.make(Book, title="ZZZ")

        url = reverse('books:book-list') + f'?q=z'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertFalse("No books found" in str(response.content))
        self.assertFalse("Alice" in str(response.content))
        self.assertTrue("ZZZ" in str(response.content))
