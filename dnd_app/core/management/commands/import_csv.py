import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template.defaultfilters import lower


class Command(BaseCommand):
    help = "Generalized command to import data from a CSV file located in <app>/initial_data/ into a model"

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name", type=str, help="The app name to import data into"
        )
        parser.add_argument(
            "model_name", type=str, help="The model name to import data into"
        )
        parser.add_argument("csv_file", type=str, help="The name of the CSV file")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"]
        app_name = kwargs["app_name"]
        csv_file = os.path.join(
            "dnd_app", app_name, "initial_data", lower(kwargs["csv_file"])
        )

        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            self.stdout.write(
                self.style.ERROR(
                    f"Model '{model_name}' does not exist in the {app_name} app"
                )
            )
            return

        try:
            with open(csv_file, mode="r") as file:
                reader = csv.DictReader(file, delimiter=";")
                created = 0
                exists = 0

                for row in reader:
                    data = {}
                    for key, value in row.items():
                        formatted_key = key.lower().replace(" ", "_")
                        if formatted_key in [f.name for f in model._meta.get_fields()]:
                            data[formatted_key] = value
                    try:
                        obj = model.objects.get(**data)
                        exists += 1
                        if settings.IMPORT_DEBUG:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"'{model_name}' object '{obj}' already exists"
                                )
                            )
                    except IntegrityError as e:
                        if "duplicate key value violates unique constraint" in str(e):
                            exists += 1
                            if settings.IMPORT_DEBUG:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"Unique constraint violation, skipping object with data: {data}"
                                    )
                                )
                        else:
                            raise
                    except model.DoesNotExist:
                        obj = model.objects.create(**data)
                        created += 1
                        if settings.IMPORT_DEBUG:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Successfully created '{model_name}' object: '{obj}'"
                                )
                            )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Finished importing '{model_name}'. Created: {created}, Already exists: {exists}"
                    )
                )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"CSV file '{csv_file}' not found"))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Validation error: {e}"))
