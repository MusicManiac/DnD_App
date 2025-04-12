from django.db import models
from django.db.models import Q


def at_least_one_not_null_field(model_name, *fields):
    """
    Creates a CheckConstraint to ensure that at least one of the given fields is not null.

    Arguments:
    - model_name: Name of the model to include in the constraint name.
    - fields: One or more field names to be checked.

    Returns:
    - A CheckConstraint that enforces at least one of the fields is not null.
    """
    # Q object with the condition that >= 1 fields is not null
    condition = [Q(**{f"{field}__isnull": False}) for field in fields]

    combined_condition = Q()
    for cond in condition:
        combined_condition |= cond

    return models.CheckConstraint(
        condition=combined_condition,
        name=f"at_least_one_not_null_{model_name}_{'_'.join(fields)}",
    )
