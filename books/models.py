from django.conf import settings
from django.db import models
from django.utils import timezone


# class Author(models.Model):
#     name = models.CharField(max_length=255)

# TODO: add Author later


class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('pricing.Category', on_delete=models.CASCADE)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = ["title", ]

    def __str__(self):
        return self.title


class BookRent(models.Model):
    class Status:
        PENDING = 0
        RENTED = 1
        RETURNED = 2

    STATUS_NAMES = {
        Status.PENDING: 'pending',
        Status.RENTED: 'rented',
        Status.RETURNED: 'returned',
    }

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    created = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    status = models.PositiveSmallIntegerField(default=Status.PENDING)

    def __str__(self):
        return f"{self.customer} rent {self.book}"

    @property
    def days_rented(self):
        if self.status == self.Status.RENTED:
            today = timezone.now().date()
            return (today - self.created).days + 1
        return 0

    @property
    def price_per_book(self):
        days = self.days_rented
        cat = self.book.category
        minimum_amount = cat.amount * cat.period_limit
        if days <= cat.period_limit:
            price = cat.amount * days
            if price < minimum_amount:
                price = minimum_amount
        else:
            rest_days = days - cat.period_limit
            price = cat.amount * cat.period_limit + cat.changed_amount * rest_days
        return price

    def finish_rent(self):
        self.status = BookRent.Status.RETURNED
        self.end = timezone.now().date()
        self.save()
