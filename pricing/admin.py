from django.contrib import admin

from .models import Currency, Category


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
