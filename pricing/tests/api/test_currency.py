import json
from model_mommy import mommy

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from pricing.models import Currency, Category

User = get_user_model()


class TestCurrencyApi(TestCase):
    def setUp(self):
        self.api_url = reverse("pricing-api:currency")

    def test_currency_empty_list(self):
        Category.objects.all().delete()
        Currency.objects.all().delete()
        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([], json.loads(response.content))

    def test_currencies(self):
        currency1 = Currency.get_default_currency()
        mommy.make(Currency, code="GBP", name="Pound sterning", symbol="£")

        response = self.client.get(self.api_url)
        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))

        for detail in content:
            if detail['id'] == currency1.id:
                self.assertEqual(detail['code'], "USD")
            else:
                self.assertEqual(detail['code'], "GBP")

    def test_currency_create(self):
        objects_count = Currency.objects.count()

        data = {
            'name': 'Test Currency',
            'symbol': 'X',
            'code': 'ABC',
        }

        response = self.client.post(self.api_url, data=data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(objects_count + 1, Currency.objects.count())

        data = {
            'name': 'Test Currency',
            'symbol': 'X',
            'code': 'ABC',
        }

        response = self.client.post(self.api_url, data=data, format='json')
        # currency with this code already exists.
        self.assertEqual(400, response.status_code)
