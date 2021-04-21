from books.models import Book

from rest_framework import serializers

from pricing.models import Category


class BookSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(view_name='pricing-api:category',
                                                   queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'category',
        )
