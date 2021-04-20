from books import views

from django.contrib.auth.decorators import login_required
from django.urls import path


app_name = 'books'

urlpatterns = [
    path('list/', login_required(views.BookListView.as_view()), name='book-list'),
    path('recipe/', login_required(views.ReceitView.as_view()), name='book-recipe'),
    path('rent/', login_required(views.BookRentView.as_view()), name='book-rent'),
]
