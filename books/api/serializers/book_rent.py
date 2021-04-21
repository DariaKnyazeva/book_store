from books.models import BookRent, Book

from rest_framework import serializers


class BookRentSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.HyperlinkedRelatedField(view_name='books-api:book', queryset=Book.objects.all())

    class Meta:
        model = BookRent
        fields = (
            'id',
            'book', 'created',
            'end_date', 'status',
        )
