import pytest

from skill.models import Skill


@pytest.fixture()
def skill_fixture(ability_fixture):
    return Skill.objects.bulk_create(
        [
            Skill(
                name="Coding",
                trained_only=False,
                armor_check_penalty=False,
                description="Doing da thing",
                link="https://dontasktoask.com/",
                ability=ability_fixture[0],
            ),
            Skill(
                name="Swimming",
                trained_only=False,
                armor_check_penalty=True,
                description="Woop woop",
                link="https://sumfunnelink.com/",
                ability=ability_fixture[1],
            ),
            Skill(
                name="Craft (Weaponsmithing)",
                trained_only=False,
                armor_check_penalty=True,
                description="Smith",
                link="https://sumfunnelink.com/",
                ability=ability_fixture[1],
            ),
        ]
    )
