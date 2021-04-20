from books.models import Book

from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):
    help = 'Generates test data (books).'

    def handle(self, *args, **options):
        Book.objects.all().delete()

        fake = Faker()
        Book.objects.bulk_create([
            Book(title=fake.sentence())
            for _ in range(10_000)
        ])
