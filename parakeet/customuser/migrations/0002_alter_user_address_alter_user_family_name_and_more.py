# Generated by Django 4.1.8 on 2023-04-28 10:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customuser", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name="user",
            name="family_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="user",
            name="given_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]