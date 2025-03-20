from django.conf import settings
from django.core.management.base import BaseCommand
from character.models import Attribute, AttributeModifier


class Command(BaseCommand):
    help = "Creates attributes modifiers ranging from -arg1 to +arg2"

    def add_arguments(self, parser):
        parser.add_argument(
            "min_value", type=int, help="Minimum value of the attribute modifier"
        )
        parser.add_argument(
            "max_value", type=int, help="Maximum value of the attribute modifier"
        )

    def handle(self, *args, **kwargs):
        min_value = kwargs["min_value"]
        max_value = kwargs["max_value"]

        created = 0
        exists = 0
        for attribute in Attribute.objects.all():
            for value in range(min_value, max_value + 1):
                if value == 0:
                    continue
                attribute_modifier, created_flag = (
                    AttributeModifier.objects.get_or_create(
                        value=value, attribute=attribute
                    )
                )
                if created_flag:
                    created += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created attribute modifier: {attribute_modifier}"
                            )
                        )
                else:
                    exists += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Attribute modifier {attribute_modifier} already exists"
                            )
                        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished generating attribute modifiers... Created: {created}, Exists: {exists}"
            )
        )
