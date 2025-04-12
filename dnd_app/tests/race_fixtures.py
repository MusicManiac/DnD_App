import pytest

from race.models import (
    AbilityModifier,
    Size,
    CharacterType,
    CharacterTypeTrait,
    Race,
    RaceType,
    RaceAbilityModifier,
    RaceTrait,
    RaceLanguage,
    RaceFavoredClass,
)
from tests.common_fixtures import source_fixture


@pytest.fixture()
def ability_modifier_fixture(ability_fixture):
    return AbilityModifier.objects.bulk_create(
        [
            AbilityModifier(value=2, ability=ability_fixture[0]),
            AbilityModifier(value=-1, ability=ability_fixture[1]),
            AbilityModifier(value=3, ability=ability_fixture[2]),
        ]
    )


@pytest.fixture()
def size_fixture():
    return Size.objects.bulk_create(
        [
            Size(
                name="Small",
                size_modifier=1,
                grapple_modifier=-1,
                height_or_length="2-4 ft",
                weight="20-40 lbs",
                space_ft=5.0,
                natural_reach_tall_ft=0,
                natural_reach_long_ft=0,
            ),
            Size(
                name="Medium",
                size_modifier=0,
                grapple_modifier=0,
                height_or_length="4-8 ft",
                weight="50-150 lbs",
                space_ft=5.0,
                natural_reach_tall_ft=0,
                natural_reach_long_ft=0,
            ),
            Size(
                name="Large",
                size_modifier=-2,
                grapple_modifier=2,
                height_or_length="8-16 ft",
                weight="200-800 lbs",
                space_ft=10.0,
                natural_reach_tall_ft=10,
                natural_reach_long_ft=10,
            ),
        ]
    )


@pytest.fixture()
def character_type_fixture():
    return CharacterType.objects.bulk_create(
        [
            CharacterType(name="Humanoid"),
            CharacterType(name="Undead"),
            CharacterType(name="Construct"),
            CharacterType(name="Dragon"),
        ]
    )


@pytest.fixture()
def character_type_trait_fixture(character_type_fixture, trait_fixture):
    return [
        CharacterTypeTrait.objects.create(
            character_type=character_type_fixture[0], trait=trait_fixture[0]
        ),
        CharacterTypeTrait.objects.create(
            character_type=character_type_fixture[1], trait=trait_fixture[1]
        ),
        CharacterTypeTrait.objects.create(
            character_type=character_type_fixture[2], trait=trait_fixture[1]
        ),
        CharacterTypeTrait.objects.create(
            character_type=character_type_fixture[3], trait=trait_fixture[1]
        ),
    ]


@pytest.fixture()
def race_fixture(size_fixture, source_fixture):
    return [
        Race.objects.create(
            name="Human",
            description="Sum desc",
            link="https://www.human.com",
            level_adjustment=0,
            size=size_fixture[1],
            source=source_fixture[0],
        ),
        Race.objects.create(
            name="Human222",
            description="Sum desc222",
            link="https://www.human.com",
            level_adjustment=0,
            size=size_fixture[1],
            source=source_fixture[0],
        ),
        Race.objects.create(
            name="Human3333",
            description="Sum desc",
            link="https://www.human.com",
            level_adjustment=0,
            size=size_fixture[2],
            source=source_fixture[1],
        ),
    ]


@pytest.fixture()
def race_type_fixture(race_fixture, character_type_fixture):
    return [
        RaceType.objects.create(
            race=race_fixture[0], character_type=character_type_fixture[0]
        ),
        RaceType.objects.create(
            race=race_fixture[1], character_type=character_type_fixture[1]
        ),
        RaceType.objects.create(
            race=race_fixture[2], character_type=character_type_fixture[2]
        ),
    ]


@pytest.fixture()
def race_ability_modifier_fixture(race_fixture, ability_modifier_fixture):
    return [
        RaceAbilityModifier.objects.create(
            race=race_fixture[0], ability_modifier=ability_modifier_fixture[0]
        ),
        RaceAbilityModifier.objects.create(
            race=race_fixture[1], ability_modifier=ability_modifier_fixture[1]
        ),
        RaceAbilityModifier.objects.create(
            race=race_fixture[2], ability_modifier=ability_modifier_fixture[2]
        ),
    ]


@pytest.fixture()
def race_trait_fixture(race_fixture, trait_fixture):
    return [
        RaceTrait.objects.create(
            race=race_fixture[0], trait=trait_fixture[0], additional_value="Some value"
        ),
        RaceTrait.objects.create(race=race_fixture[1], trait=trait_fixture[1]),
        RaceTrait.objects.create(race=race_fixture[2], trait=trait_fixture[1]),
    ]


@pytest.fixture()
def race_language_fixture(race_fixture, language_fixture):
    return [
        RaceLanguage.objects.create(
            race=race_fixture[0], language=language_fixture[0], is_automatic=True
        ),
        RaceLanguage.objects.create(race=race_fixture[1], language=language_fixture[1]),
        RaceLanguage.objects.create(race=race_fixture[2], language=language_fixture[1]),
    ]


@pytest.fixture()
def race_favored_class_fixture(race_fixture, character_class_fixture):
    return [
        RaceFavoredClass.objects.create(
            race=race_fixture[0],
            character_class=character_class_fixture[0],
        ),
        RaceFavoredClass.objects.create(
            race=race_fixture[1], character_class=character_class_fixture[1]
        ),
        RaceFavoredClass.objects.create(
            race=race_fixture[2], character_class=character_class_fixture[1]
        ),
    ]
