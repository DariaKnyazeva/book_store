from rest_framework import generics

from books.api.serializers.book_rent import BookRentSerializer
from books.models import BookRent


__all__ = [
    'ListCreateBookRentView',
    'RetrieveBookRentView',
]


class BaseView:
    serializer_class = BookRentSerializer
    queryset = BookRent.objects.all().select_related('book', 'customer', 'price').order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customer_id=self.request.user.id)


class ListCreateBookRentView(BaseView, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class RetrieveBookRentView(BaseView, generics.RetrieveAPIView):
    pass
