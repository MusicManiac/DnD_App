#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dnd_app"))


if __name__ == "__main__":
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnd_app.core.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
