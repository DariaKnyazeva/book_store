from django.contrib import admin

from .models import Book, BookRent


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(BookRent)
class BookRentAdmin(admin.ModelAdmin):
    pass
