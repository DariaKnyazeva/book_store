from books.api import views

from django.urls import path

app_name = 'books-api'


urlpatterns = [
    path('books/', views.ListCreateBookView.as_view(), name='books'),
    path('books/<int:pk>/', views.RetrieveBookView.as_view(), name='book'),

    path('book-rents/', views.ListCreateBookRentView.as_view(), name='book-rents'),
    path('book-rents/<int:pk>/', views.RetrieveBookRentView.as_view(), name='book-rent'),
]
