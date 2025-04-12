import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Deletes all migration files in the project"

    def handle(self, *args, **kwargs):
        confirmation = input(
            "Are you REALLY sure you want to delete all migration files? (yes/no): "
        ).lower()

        if confirmation != "yes":
            self.stdout.write(
                self.style.SUCCESS(
                    "Operation canceled. Migration files were not deleted."
                )
            )
            return

        for app in settings.MY_APPS:
            try:
                app_path = os.path.join(settings.BASE_DIR, app.replace(".", "/"))
                migrations_dir = os.path.join(app_path, "migrations")
                if not os.path.isdir(migrations_dir):
                    continue
                for migration_file in glob.glob(os.path.join(migrations_dir, "*.py")):
                    if not migration_file.endswith("__init__.py"):
                        os.remove(migration_file)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Deleted migration file: {migration_file}"
                            )
                        )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error while deleting migrations in {app}: {e}")
                )
