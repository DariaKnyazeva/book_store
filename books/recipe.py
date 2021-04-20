from django.utils import timezone

from pricing.models import Currency
from .models import BookRent


class Recipe:
    """
    Service class to calculate Customer's recipy
    """

    def __init__(self, customer):
        self.customer = customer

    def caclulate_price(self):
        """
        The rent is calculated on the basis of the number of books rented
        and durations for each book it was rented.
        Per day rental charge is $ 1.
        """
        today = timezone.now().date()
        rents = BookRent.objects.filter(customer=self.customer,
                                        status=BookRent.Status.RENTED)
        return sum([((today - rent.created).days + 1) * rent.price.amount for rent in rents])

    def get_price(self):
        """
        Returns string representation of price with the currency symbol
        """
        # TODO: the currency has to be customizable
        currency = Currency.get_default_currency()
        price = self.caclulate_price()
        return f"{currency.symbol} {price:.2f}"
