# Generated by Django 4.1.8 on 2023-04-17 00:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quickstart", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeeksModel",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name="Hero",
        ),
    ]
