from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Runs all import commands"

    def handle(self, *args, **kwargs):
        # Bulk imports with import_character_csvs
        self.stdout.write(self.style.NOTICE("Running import_character_csvs..."))

        self.stdout.write(self.style.NOTICE("Importing TraitClassification..."))
        call_command(
            "import_character_csvs",
            "TraitClassification",
            "trait_classification_list.csv",
        )

        self.stdout.write(self.style.NOTICE("Importing Alignment..."))
        call_command("import_character_csvs", "Alignment", "alignment_list.csv")

        self.stdout.write(self.style.NOTICE("Importing Size..."))
        call_command("import_character_csvs", "Size", "size_list.csv")

        self.stdout.write(self.style.NOTICE("Importing Language..."))
        call_command("import_character_csvs", "Language", "language_list.csv")

        self.stdout.write(self.style.NOTICE("Importing Attribute..."))
        call_command("import_character_csvs", "Attribute", "attribute_list.csv")

        # 1by1 imports
        self.stdout.write(self.style.NOTICE("Importing Trait..."))
        call_command("import_trait")

        # Generators
        self.stdout.write(self.style.NOTICE("Running generate_attribute_modifier..."))
        call_command("generate_attribute_modifier", "-6", "6")

        self.stdout.write(self.style.SUCCESS("All commands ran successfully"))
