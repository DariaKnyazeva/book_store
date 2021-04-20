from pricing.models import Category

from rest_framework import serializers


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'amount', 'currency', 'period', 'name'
        )
