import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import Trait, TraitClassification


class Command(BaseCommand):
    help = "Command to import 'Trait' data from a CSV file into the 'Trait' model"

    def handle(self, *args, **kwargs):
        # Cache TraitClassification to avoid querying the database multiple times
        trait_classification_dict = {
            bonus.name: bonus.id for bonus in TraitClassification.objects.all()
        }

        with open("dnd_app/common/initial_data/trait_list.csv", mode="r") as file:
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

                try:
                    trait = Trait.objects.get(
                        short_description=row["Short Description"]
                    )
                    exists += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Trait '{trait.short_description}' already exists"
                            )
                        )
                except Trait.DoesNotExist:
                    trait = Trait.objects.create(
                        short_description=row["Short Description"],
                        long_description=row["Long Description"],
                        link=row["Link"],
                        trait_classification_id=trait_classification_id,
                    )
                    created += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created Trait: '{trait.short_description}'"
                            )
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Finished importing 'Trait'. Created: {created}, Already exists: {exists}"
                )
            )
