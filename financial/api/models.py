from django.db import models


class FinancialData(models.Model):
    symbol = models.CharField(
        max_length=10, blank=False, null=False
    )
    date = models.DateField(
         blank=False, null=False
    )
    open_price = models.FloatField(default=0, blank=False, null=False)
    close_price = models.FloatField(default=0, blank=False, null=False)
    volume = models.BigIntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = "financial_data"
        constraints = [
            models.UniqueConstraint(fields=['symbol', 'date'], name='symbol_date_unique')
        ]