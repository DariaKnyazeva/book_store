
from books.api.serializers.book import BookSerializer
from books.models import Book

from rest_framework import generics


__all__ = [
    'ListCreateBookView',
    'RetrieveBookView',
]


class ListCreateBookView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class RetrieveBookView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
