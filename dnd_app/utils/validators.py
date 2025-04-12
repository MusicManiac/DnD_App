from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = datetime.now().year
    if value < 1974 or value > current_year:
        raise ValidationError(f"Year must be between 1974 and {current_year}.")


def validate_integer_in_range(value, min_value=None, max_value=None):
    if value > max_value or value < min_value:
        raise ValidationError(f"Value must be between {min_value} and {max_value}.")


def validate_positive_integer(value):
    if value < 0:
        raise ValidationError("Value must be a positive integer.")
