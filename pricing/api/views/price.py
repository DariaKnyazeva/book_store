
from pricing.api.serializers.price import PriceSerializer
from pricing.models import Price

from rest_framework import generics


__all__ = [
    'ListCreatePriceView',
    'RetrievePriceView',
]


class ListCreatePriceView(generics.ListCreateAPIView):
    serializer_class = PriceSerializer
    queryset = Price.objects.all()


class RetrievePriceView(generics.RetrieveAPIView):
    serializer_class = PriceSerializer
    queryset = Price.objects.all()
