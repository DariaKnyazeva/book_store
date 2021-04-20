from books import views

from django.urls import path


app_name = 'books'

urlpatterns = [
    path('list/', views.BookListView.as_view(), name='book-list'),
    path('recipe/', views.ReceitView.as_view(), name='book-recipe'),
]
