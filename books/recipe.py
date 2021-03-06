from pricing.models import Currency
from .models import BookRent


class Recipe:
    """
    Service class to calculate Customer's receipt
    """

    def __init__(self, customer):
        self.customer = customer
        self.rents = BookRent.objects.filter(customer=self.customer,
                                             status=BookRent.Status.RENTED).\
            select_related('book', 'book__category')

    def caclulate_price(self):
        """
        The rent is calculated on the basis of the number of books rented
        and durations for each book it was rented.
        The rent is also category specific and it changes after days limit is hit.
        There is also a minimum charge limit per category.
        """
        price = sum(rent.price_and_details[0] for rent in self.rents)
        return price

    def get_price_repr(self):
        """
        Returns string representation of price with the currency symbol
        """
        # TODO: the currency has to be customizable based on the Book store
        currency = Currency.get_default_currency()
        price = self.caclulate_price()
        return f"{currency.symbol} {price:.2f}"
