
from pricing.api.serializers.price import PriceSerializer
from pricing.models import Category

from rest_framework import generics


__all__ = [
    'ListCreatePriceView',
    'RetrievePriceView',
]


class ListCreatePriceView(generics.ListCreateAPIView):
    serializer_class = PriceSerializer
    queryset = Category.objects.all()


class RetrievePriceView(generics.RetrieveAPIView):
    serializer_class = PriceSerializer
    queryset = Category.objects.all()
