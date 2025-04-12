import glob
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Lowercases names of all import files and then runs all import commands"

    def lowercase_import_files(self):
        """
        This method lowercases all files inside initial_data folders
        """
        for app in settings.MY_APPS:
            try:
                app_path = os.path.join(settings.BASE_DIR, app.replace(".", "/"))
                migrations_dir = os.path.join(app_path, "initial_data")
                if not os.path.isdir(migrations_dir):
                    continue
                for migration_file in glob.glob(os.path.join(migrations_dir, "*.csv")):
                    filename = os.path.basename(migration_file)
                    if (
                        not migration_file.endswith("__init__.py")
                        and filename != filename.lower()
                    ):
                        os.rename(migration_file, migration_file.lower())
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Lowercased import file: {migration_file}"
                            )
                        )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error while renaming import files in {app}: {e}")
                )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Lowercasing import files..."))
        self.lowercase_import_files()

        # Bulk imports with import_csv and import_json

        self.stdout.write(self.style.NOTICE("Importing Die..."))
        call_command("import_csv", "common", "Die", "Die_list.csv")

        self.stdout.write(self.style.NOTICE("Importing DurationUnit..."))
        call_command("import_csv", "common", "DurationUnit", "DurationUnit_list.csv")

        self.stdout.write(self.style.NOTICE("Importing Source..."))
        call_command("import_csv", "common", "Source", "Source_list.csv")

        self.stdout.write(self.style.NOTICE("Importing BABProgression..."))
        call_command(
            "import_json",
            "character_class",
            "BABProgression",
            "babprogression_list.json",
        )

        self.stdout.write(self.style.NOTICE("Importing TraitClassification..."))
        call_command(
            "import_csv",
            "common",
            "TraitClassification",
            "TraitClassification_list.csv",
        )

        self.stdout.write(self.style.NOTICE("Importing Alignment..."))
        call_command("import_csv", "common", "Alignment", "Alignment_list.csv")

        self.stdout.write(self.style.NOTICE("Importing Ability..."))
        call_command("import_csv", "common", "Ability", "Ability_list.csv")

        self.stdout.write(self.style.NOTICE("Importing BSBProgression..."))
        call_command("import_bsbprogression")

        self.stdout.write(self.style.NOTICE("Importing Skill..."))
        call_command("import_skill")

        self.stdout.write(self.style.NOTICE("Importing Size..."))
        call_command("import_csv", "race", "Size", "Size_list.csv")

        self.stdout.write(self.style.NOTICE("Importing MagicAuraStrength..."))
        call_command(
            "import_csv", "spell", "MagicAuraStrength", "MagicAuraStrength_list.csv"
        )

        self.stdout.write(self.style.NOTICE("Importing MagicSchool..."))
        call_command("import_csv", "spell", "MagicSchool", "MagicSchool_list.csv")

        self.stdout.write(self.style.NOTICE("Importing MagicSubSchool..."))
        call_command("import_csv", "spell", "MagicSubSchool", "MagicSubSchool_list.csv")

        self.stdout.write(self.style.NOTICE("Importing SpellDescriptor..."))
        call_command(
            "import_csv", "spell", "SpellDescriptor", "SpellDescriptor_list.csv"
        )

        self.stdout.write(self.style.NOTICE("Importing SpellComponent..."))
        call_command("import_csv", "spell", "SpellComponent", "SpellComponent_list.csv")

        self.stdout.write(self.style.NOTICE("Importing CastingTime..."))
        call_command("import_csv", "spell", "CastingTime", "CastingTime_list.csv")

        self.stdout.write(self.style.NOTICE("Importing SpellRange..."))
        call_command("import_csv", "spell", "SpellRange", "SpellRange_list.csv")

        self.stdout.write(self.style.NOTICE("Importing ItemCategory..."))
        call_command("import_csv", "item", "ItemCategory", "ItemCategory_list.csv")

        self.stdout.write(self.style.NOTICE("Importing WeaponCategory..."))
        call_command("import_csv", "item", "WeaponCategory", "WeaponCategory_list.csv")

        self.stdout.write(self.style.NOTICE("Importing WeaponDamageType..."))
        call_command(
            "import_csv", "item", "WeaponDamageType", "WeaponDamageType_list.csv"
        )

        self.stdout.write(self.style.NOTICE("Importing ArmorType..."))
        call_command("import_csv", "item", "ArmorType", "ArmorType_list.csv")

        self.stdout.write(self.style.NOTICE("Importing SpecialMaterial..."))
        call_command(
            "import_csv", "item", "SpecialMaterial", "SpecialMaterial_list.csv"
        )

        self.stdout.write(self.style.NOTICE("Importing Language..."))
        call_command("import_csv", "common", "Language", "Language_list.csv")

        self.stdout.write(self.style.NOTICE("Importing TypeOfFeat..."))
        call_command("import_csv", "feat", "TypeOfFeat", "TypeOfFeat_list.csv")

        self.stdout.write(self.style.NOTICE("Importing Trait..."))
        call_command("import_trait")

        self.stdout.write(self.style.NOTICE("Running generate_ability_modifier..."))
        call_command("generate_ability_modifier", "-6", "6")

        self.stdout.write(self.style.SUCCESS("All commands ran successfully"))
