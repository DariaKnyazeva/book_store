import random

from books.models import Book, BookRent
from pricing.models import Currency, Category
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
        Category.objects.all().delete()

        curr = Currency.get_default_currency()

        reg, _ = Category.objects.get_or_create(
            name="Regular", amount=1.0, changed_amount=1.5,
            period_limit=2,
            currency=curr
        )
        fic, _ = Category.objects.get_or_create(
            name="Fiction", amount=4.5, changed_amount=5,
            currency=curr,
            period_limit=3,
        )
        nov, _ = Category.objects.get_or_create(
            name="Novel", amount=1.5, changed_amount=2.0,
            currency=curr,
            period_limit=2
        )

        cats = [reg, fic, nov]

        now = timezone.now()
        try:
            User.objects.get(username="daria").delete()
        except User.DoesNotExist:
            pass
        user = User(username="daria",
                    is_staff=True, is_active=True, is_superuser=True,
                    last_login=now, date_joined=now, user_role=1)
        user.set_password("qwerty")
        user.save()

        fake = Faker()
        Book.objects.bulk_create([
            Book(title=fake.sentence(), category=random.choice(cats))
            for _ in range(10_000)
        ])

        books = Book.objects.filter(title__startswith="Abl")
        print(f"Create {books.count()} rents")
        for book in books:
            rent = BookRent.objects.create(book=book, customer=user,
                                           status=BookRent.Status.RENTED)
            rent.created = now - timedelta(days=2)
            rent.save()
