from django.contrib import admin

from .models import BookRent


@admin.register(BookRent)
class BookRentAdmin(admin.ModelAdmin):
    pass
