import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.exceptions import ValidationError

from common.models import Ability


class Command(BaseCommand):
    help = "Command to import BSBProgression data from a JSON file located in character_class/initial_data/ into a model"

    def handle(self, *args, **kwargs):
        model_name = "BSBProgression"
        app_name = "character_class"
        json_file = "dnd_app/character_class/initial_data/bsbprogression_list.json"

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

                ability_dict = {
                    "Wisdom": ("Wil", ability.id)
                    for ability in Ability.objects.filter(name="Wisdom")
                }
                ability_dict.update(
                    {
                        "Dexterity": ("Reflex", ability.id)
                        for ability in Ability.objects.filter(name="Dexterity")
                    }
                )
                ability_dict.update(
                    {
                        "Constitution": ("Fortitude", ability.id)
                        for ability in Ability.objects.filter(name="Constitution")
                    }
                )

                for entry_key, entry_data in data.items():
                    original_name = entry_data["name"]
                    for ability_name, (
                        display_name,
                        ability_id,
                    ) in ability_dict.items():
                        entry_data["name"] = f"{display_name} ({original_name})"
                        entry_data["ability_id"] = ability_id
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
