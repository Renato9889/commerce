# Generated by Django 4.2.2 on 2023-08-28 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_watchlistitem_id"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="user_name",),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
