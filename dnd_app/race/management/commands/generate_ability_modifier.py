from django.conf import settings
from django.core.management.base import BaseCommand
from race.models import AbilityModifier
from common.models import Ability


class Command(BaseCommand):
    help = "Creates ability modifiers ranging from -arg1 to +arg2"

    def add_arguments(self, parser):
        parser.add_argument(
            "min_value", type=int, help="Minimum value of the ability modifier"
        )
        parser.add_argument(
            "max_value", type=int, help="Maximum value of the ability modifier"
        )

    def handle(self, *args, **kwargs):
        min_value = kwargs["min_value"]
        max_value = kwargs["max_value"]

        created = 0
        exists = 0
        for ability in Ability.objects.all():
            for value in range(min_value, max_value + 1):
                if value == 0:
                    continue
                ability_modifier, created_flag = AbilityModifier.objects.get_or_create(
                    value=value, ability=ability
                )
                if created_flag:
                    created += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created ability modifier: {ability_modifier}"
                            )
                        )
                else:
                    exists += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Ability modifier {ability_modifier} already exists"
                            )
                        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished generating ability modifiers... Created: {created}, Exists: {exists}"
            )
        )
