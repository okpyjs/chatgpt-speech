import json

from django.core.management.base import BaseCommand
from plan.models import Currency, Plan


class Command(BaseCommand):
    help = "Load data from JSON file"

    def handle(self, *args, **options):
        filename = "mydata.json"
        with open(filename) as f:
            data = json.load(f)
            for item in data:
                if item["model"] == "Plan.Currency":
                    Currency.objects.create(**item["fields"])
                if item["model"] == "Plan.Plan":
                    Plan.objects.create(**item["fields"])
