# Generated by Django 4.1.8 on 2023-04-19 09:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("plan", "0009_alter_gpt_model_description"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PayUnit",
            new_name="Currency",
        ),
    ]
