from books.models import Book, BookRent
from pricing.models import Currency, Price
from users.models import User

from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import timedelta
from faker import Faker


class Command(BaseCommand):
    help = 'Generates test data (books).'

    def handle(self, *args, **options):
        BookRent.objects.all().delete()
        Book.objects.all().delete()
        Price.objects.all().delete()

        currency = Currency.get_default_currency()
        price, _cr = Price.objects.get_or_create(currency=currency, amount=1)

        now = timezone.now()
        User.objects.get(username="daria").delete()
        user = User(username="daria",
                    is_staff=True, is_active=True, is_superuser=True,
                    last_login=now, date_joined=now, user_role=1)
        user.set_password("qwerty")
        user.save()

        fake = Faker()
        Book.objects.bulk_create([
            Book(title=fake.sentence())
            for _ in range(10_000)
        ])

        z_books = Book.objects.filter(title__startswith="Abl")
        print("Create {} rents".format(z_books.count()))
        for book in z_books:
            rent = BookRent.objects.create(book=book, customer=user, price=price,
                                           status=BookRent.Status.RENTED)
            rent.created = now - timedelta(days=2)
            rent.save()
