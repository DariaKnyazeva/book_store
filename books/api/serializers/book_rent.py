from books.models import BookRent

from rest_framework import serializers


class BookRentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookRent
        fields = (
            'id',
            'customer', 'book', 'created',
            'price', 'end_date', 'status',
        )
