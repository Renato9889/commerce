# Generated by Django 4.2.2 on 2023-08-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_watchlistitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="watchlistitem",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
