from rest_framework import serializers

from .models import (
    FinancialData
)


class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = [
            "symbol",
            "date",
            "open_price",
            "close_price",
            "volume"
        ]
