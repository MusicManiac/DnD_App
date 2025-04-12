import pytest


@pytest.mark.django_db
def test_source_creation(source_fixture):
    source = source_fixture[0]
    assert source.name == "PHB"
    assert source.year == 2003
    assert source.description == "Player's Handbook"
    assert str(source) == "PHB"


@pytest.mark.django_db
def test_die_creation(die_fixture):
    assert die_fixture[2].sides == 6
    assert str(die_fixture[2]) == "d6"


@pytest.mark.django_db
def test_trait_classification_creation(trait_classification_fixture):
    classification = trait_classification_fixture[0]
    assert classification.name == "Vision and Senses"
    assert (
        classification.description
        == "Some kind of vision or senses bonus such as darkvision or tremorsense"
    )
    assert str(classification) == "Vision and Senses"


@pytest.mark.django_db
def test_trait_creation(trait_fixture, trait_classification_fixture):
    classification = trait_classification_fixture[0]
    trait = trait_fixture[0]
    assert trait.short_description == "Darkvision"
    assert trait.long_description == "Ability to see in the dark."
    assert trait.trait_classification == classification
    assert str(trait) == "Darkvision"


@pytest.mark.django_db
def test_duration_unit_creation(duration_unit_fixture):
    duration_unit = duration_unit_fixture[0]
    assert duration_unit.name == "Second"
    assert duration_unit.name_plural == "Seconds"
    assert duration_unit.duration_in_seconds == 1
    assert str(duration_unit) == "Second"


@pytest.mark.django_db
def test_ability_creation(ability_fixture):
    ability = ability_fixture[0]
    assert ability.name == "Strength"
    assert ability.abbreviation == "STR"
    assert ability.description == "Me strong, me smash!"
    assert str(ability) == "Strength"


@pytest.mark.django_db
def test_alignment_creation(alignment_fixture):
    alignment = alignment_fixture[0]
    assert alignment.name == "Lawful Good"
    assert alignment.abbreviation == "LG"
    assert alignment.description == "Paladin and stuff"
    assert str(alignment) == "Lawful Good"


@pytest.mark.django_db
def test_language_creation(language_fixture, source_fixture):
    language = language_fixture[0]
    source = source_fixture[0]
    assert language.name == "Common"
    assert language.alphabet == "Common"
    assert not language.is_secret
    assert language.source == source
    assert str(language) == "Common"
