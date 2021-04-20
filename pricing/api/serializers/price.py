from pricing.models import Price

from rest_framework import serializers


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Price
        fields = (
            'id', 'amount', 'currency', 'period',
        )
