import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import FinancialData
import os
from datetime import datetime, timedelta


class Command(BaseCommand):
    def fetch_date_from_api(self, symbol):
        """
        Download data using AlphaVantage API.
        Data definition has field name 'Time Series (Daily)'
        which was considered to accept for saving in DB
        """
        api_key = os.environ.get("API_KEY", None)

        if not api_key:
            raise ValueError("API Key was not found!")

        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "apikey": api_key,
        }

        r = requests.get(url, params=params)
        data = r.json()

        data = data.get("Time Series (Daily)", None)
        return data

    def data_clean(self, symbol, data):
        # get date prior two weeks to filter data
        weeks_prior = datetime.now() - timedelta(weeks=2)

        dl = []
        for i in data:
            if datetime.strptime(i, "%Y-%m-%d") >= weeks_prior:
                row = data[i]
                d_dict = dict(
                    date=i,
                    symbol=symbol,
                    open_price=row.get("1. open", 0),
                    close_price=row.get("4. close", 0),
                    volume=row.get("6. volume", 0),
                )
                dl.append(d_dict)
        return dl

    def handle(self, *args, **options):
        """
        Iterate to symbols of IBM and Apple Inc to gat data from AlphaVantage
        """
        try:
            symbols = ["IBM", "AAPL"]
            fin_df = []

            for s in symbols:
                data = self.fetch_date_from_api(s)

                if data:
                    df = self.data_clean(s, data)
                    fin_df = fin_df + df

            # Bulk save
            dl = []
            with transaction.atomic():
                for d in fin_df:
                    f = FinancialData()
                    f.symbol = d.get("symbol")
                    f.date = d.get("date")
                    f.open_price = d.get("open_price")
                    f.close_price = d.get("close_price")
                    f.volume = d.get("volume")

                    dl.append(f)

            _ = FinancialData.objects.bulk_create(dl)

            print("-- SUCCESS: Data was imported --")
        except Exception as err:
            print(f"-- ERROR: {err} --")
