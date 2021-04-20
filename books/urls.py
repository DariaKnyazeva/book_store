from books import views

from django.urls import path


app_name = 'books'

urlpatterns = [
    path('book/list/', views.BookListView.as_view(), name='book-list'),
]
