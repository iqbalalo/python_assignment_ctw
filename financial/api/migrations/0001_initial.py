# Generated by Django 4.2 on 2023-04-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FinancialData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("symbol", models.CharField(max_length=10)),
                ("date", models.DateField()),
                ("open_price", models.FloatField(default=0)),
                ("close_price", models.FloatField(default=0)),
                ("volume", models.BigIntegerField(default=0)),
            ],
            options={
                "db_table": "financial_data",
            },
        ),
        migrations.AddConstraint(
            model_name="financialdata",
            constraint=models.UniqueConstraint(
                fields=("symbol", "date"), name="symbol_date_unique"
            ),
        ),
    ]
