from django.core.validators import MinValueValidator
from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name

    @classmethod
    def get_default_currency(cls):
        currency, _ = cls.objects.get_or_create(
            code="USD", defaults={"name": "US Dollar", "symbol": "$"}
        )
        return currency


class Price(models.Model):
    class PricePeriod:
        MINUTE = 1
        HOUR = 2
        DAY = 3
        MONTH = 4
        YEAR = 5

    PRICE_PERIODS = (
        (PricePeriod.MINUTE, "Minute"),
        (PricePeriod.HOUR, "Hour"),
        (PricePeriod.DAY, "Day"),
        (PricePeriod.MONTH, "Month"),
        (PricePeriod.YEAR, "Year"),
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=1.0,
                                 validators=[MinValueValidator(0.01)],
                                 help_text="The price amount for the period unit")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    period = models.PositiveSmallIntegerField(choices=PRICE_PERIODS,
                                              default=PricePeriod.DAY)

    class Meta:
        abstract = True


class Category(Price):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name
