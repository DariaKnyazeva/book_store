
from pricing.api.serializers.currency import CurrencySerializer
from pricing.models import Currency

from rest_framework import generics


__all__ = [
    'ListCreateCurrencyView',
    'RetrieveCurrencyView',
]


class ListCreateCurrencyView(generics.ListCreateAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all().order_by('id')


class RetrieveCurrencyView(generics.RetrieveAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
