import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import Trait, TraitClassification, Ability
from skill.models import Skill


class Command(BaseCommand):
    help = "Command to import 'Skill' data from a CSV file into the 'Skill' model"

    def handle(self, *args, **kwargs):
        # Cache Ability to avoid querying the database multiple times
        ability_dict = {ability.name: ability.id for ability in Ability.objects.all()}

        with open("dnd_app/skill/initial_data/skill_list.csv", mode="r") as file:
            reader = csv.DictReader(file, delimiter=";")
            created = 0
            exists = 0
            for row in reader:
                ability_id = ability_dict.get(row["Ability"])

                if ability_id is None:
                    self.stdout.write(
                        self.style.ERROR(f"Ability '{row['Ability']}' not found")
                    )
                    continue

                skill, created_flag = Skill.objects.get_or_create(
                    name=row["Name"],
                    trained_only=row["Trained Only"],
                    armor_check_penalty=row["Armor Check Penalty"],
                    link=row["Link"],
                    description=row["Description"],
                    ability_id=ability_id,
                )
                if created_flag:
                    created += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created Skill: '{skill.name}'"
                            )
                        )
                else:
                    exists += 1
                    if settings.IMPORT_DEBUG:
                        self.stdout.write(
                            self.style.WARNING(f"Skill '{skill.name}' already exists")
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Finished importing 'Skill'. Created: {created}, Already exists: {exists}"
                )
            )
