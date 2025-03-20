import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from character.models import TraitClassification, Trait


class Command(BaseCommand):
    help = "Command to import 'Trait' data from a CSV file into the 'Trait' model"

    def handle(self, *args, **kwargs):
        # Cache TraitClassification to avoid querying the database multiple times
        trait_classification_dict = {
            bonus.name: bonus.id for bonus in TraitClassification.objects.all()
        }

        with open("dnd_app/character/initial_data/trait_list.csv", mode="r") as file:
            reader = csv.DictReader(file, delimiter=";")
            created = 0
            exists = 0
            for row in reader:
                trait_classification_id = trait_classification_dict.get(
                    row["Trait Classification"]
                )

                if trait_classification_id is None:
                    self.stdout.write(
                        self.style.ERROR(
                            f"TraitClassification '{row['Trait Classification']}' not found"
                        )
                    )
                    continue

                trait, created_flag = Trait.objects.get_or_create(
                    short_description=row["Short Description"],
                    long_description=row["Long Description"],
                    link=row["Link"],
                    trait_classification_id=trait_classification_id,
                )
                if created_flag:
                    created += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created TypeOrSubtypeTrait: '{trait.short_description}'"
                            )
                        )
                else:
                    exists += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.WARNING(
                                f"TypeOrSubtypeTrait '{trait.short_description}' already exists"
                            )
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Finished importing 'TypeOrSubtypeTrait'. Created: {created}, Already exists: {exists}"
                )
            )
