import json
from model_mommy import mommy

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from pricing.models import Currency, Category

User = get_user_model()


class TestCategoryApi(TestCase):
    def setUp(self):
        self.api_url = reverse("pricing-api:category")

    def test_currency_empty_list(self):
        Category.objects.all().delete()
        Currency.objects.all().delete()
        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        self.assertListEqual([], json.loads(response.content)['results'])

    def test_categories(self):
        Category.objects.all().delete()

        currency = Currency.get_default_currency()
        cat = mommy.make(Category, currency=currency, name="Fiction", amount=2,
                         changed_amount=4, period_limit=3)

        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)['results']
        self.assertEqual(1, len(content))
        self.assertEqual(cat.id, content[0]['id'])
        self.assertEqual("Fiction", content[0]['name'])
        self.assertEqual('2.00', content[0]['amount'])
        self.assertEqual('4.00', content[0]['changed_amount'])
        self.assertEqual(3, content[0]['period_limit'])

    def test_cetegory_create(self):
        objects_count = Category.objects.count()

        currency = Currency.get_default_currency()
        currency_url = "http://testserver" + reverse("pricing-api:currency", kwargs={"pk": currency.id})

        data = {
            'name': 'Test Category',
            'currency': currency_url,
            'amount': 3,
            'changed_amount': 5,
            'period_limit': 5,
        }

        response = self.client.post(self.api_url, data=data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(objects_count + 1, Category.objects.count())
