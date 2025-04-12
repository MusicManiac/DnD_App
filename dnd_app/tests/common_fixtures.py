import pytest

from common.models import (
    Source,
    Die,
    TraitClassification,
    Trait,
    DurationUnit,
    Ability,
    Alignment,
    Language,
)


@pytest.fixture()
def source_fixture():
    return Source.objects.bulk_create(
        [
            Source(
                name="PHB",
                link="https://somelink.com",
                year=2003,
                description="Player's Handbook",
            ),
            Source(
                name="DMG",
                link="https://anotherlink.com",
                year=2002,
                description="Dungeon Master's Guide",
            ),
        ]
    )


@pytest.fixture()
def die_fixture():
    return Die.objects.bulk_create([Die(sides=2), Die(sides=4), Die(sides=6)])


@pytest.fixture()
def trait_classification_fixture():
    return TraitClassification.objects.bulk_create(
        [
            TraitClassification(
                name="Vision and Senses",
                description="Some kind of vision or senses bonus such as darkvision or tremorsense",
            ),
            TraitClassification(name="Attack", description="Some kind of attack bonus"),
        ]
    )


@pytest.fixture()
def trait_fixture(trait_classification_fixture):
    return Trait.objects.bulk_create(
        [
            Trait(
                short_description="Darkvision",
                long_description="Ability to see in the dark.",
                trait_classification=trait_classification_fixture[0],
            ),
            Trait(
                short_description="+1 to attack rolls",
                trait_classification=trait_classification_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def duration_unit_fixture():
    return DurationUnit.objects.bulk_create(
        [
            DurationUnit(name="Second", name_plural="Seconds", duration_in_seconds=1),
            DurationUnit(
                name="Round",
                name_plural="Rounds",
                description="Enough time to die",
                duration_in_seconds=6,
            ),
        ]
    )


@pytest.fixture()
def ability_fixture():
    return Ability.objects.bulk_create(
        [
            Ability(
                name="Strength",
                abbreviation="STR",
                description="Me strong, me smash!",
            ),
            Ability(
                name="Dexterity",
                abbreviation="DEX",
                description="Me quick, me dodge!",
            ),
            Ability(name="Wisdom", abbreviation="WIS", description="Me wise, me see!"),
        ]
    )


@pytest.fixture()
def alignment_fixture():
    return Alignment.objects.bulk_create(
        [
            Alignment(
                id=1,
                name="Lawful Good",
                abbreviation="LG",
                description="Paladin and stuff",
            ),
            Alignment(
                id=2,
                name="Chaotic Neutral",
                abbreviation="CN",
                description="Chaotic evil pretending to be neutral.",
            ),
        ]
    )


@pytest.fixture()
def language_fixture(source_fixture):
    return Language.objects.bulk_create(
        [
            Language(id=1, name="Common", alphabet="Common", source=source_fixture[0]),
            Language(id=2, name="Elvish", source=source_fixture[1]),
        ]
    )
