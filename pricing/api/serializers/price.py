from pricing.models import Category

from rest_framework import serializers

from pricing.models import Currency


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    currency = serializers.HyperlinkedRelatedField(view_name='pricing-api:currency',
                                                   queryset=Currency.objects.all())

    class Meta:
        model = Category
        fields = (
            'id', 'amount', 'changed_amount',
            'currency', 'period', 'period_limit', 'name',
        )
