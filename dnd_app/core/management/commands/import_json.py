import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Generalized command to import data from a JSON file located in <app>/initial_data/ into a model"

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name", type=str, help="The app name to import data into"
        )
        parser.add_argument(
            "model_name", type=str, help="The model name to import data into"
        )
        parser.add_argument("json_file", type=str, help="The name of the JSON file")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"]
        app_name = kwargs["app_name"]
        json_file = os.path.join(
            "dnd_app", app_name, "initial_data", kwargs["json_file"]
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
            with open(json_file, mode="r") as file:
                data = json.load(file)
                created = 0
                exists = 0

                for entry_key, entry_data in data.items():
                    obj, created_flag = model.objects.get_or_create(**entry_data)
                    if created_flag:
                        created += 1
                        if settings.IMPORT_DEBUG:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Successfully created '{model_name}' object: '{obj}'"
                                )
                            )
                    else:
                        exists += 1
                        if settings.IMPORT_DEBUG:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"'{model_name}' object '{obj}' already exists"
                                )
                            )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Finished importing '{model_name}'. Created: {created}, Already exists: {exists}"
                    )
                )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"JSON file '{json_file}' not found"))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Validation error: {e}"))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"JSON decode error: {e}"))
