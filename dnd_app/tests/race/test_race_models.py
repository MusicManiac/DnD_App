import pytest


@pytest.mark.django_db
def test_ability_modifier_creation(ability_modifier_fixture, ability_fixture):
    ability_modifier = ability_modifier_fixture[0]
    assert ability_modifier.value == 2
    assert ability_modifier.ability == ability_fixture[0]
    assert str(ability_modifier) == f"+2 {ability_fixture[0].name}"


@pytest.mark.django_db
def test_size_creation(size_fixture):
    size = size_fixture[0]
    assert size.name == "Small"
    assert size.size_modifier == 1
    assert size.grapple_modifier == -1
    assert size.height_or_length == "2-4 ft"
    assert size.weight == "20-40 lbs"
    assert size.space_ft == 5.0
    assert size.natural_reach_tall_ft == 0
    assert size.natural_reach_long_ft == 0
    assert str(size) == "Small"


@pytest.mark.django_db
def test_character_type_creation(character_type_fixture):
    character_type = character_type_fixture[0]
    assert character_type.name == "Humanoid"
    assert str(character_type) == "Humanoid"


@pytest.mark.django_db
def test_character_type_trait_creation(character_type_trait_fixture, trait_fixture):
    character_type_trait = character_type_trait_fixture[0]
    assert (
        character_type_trait.character_type
        == character_type_trait_fixture[0].character_type
    )
    assert character_type_trait.trait == trait_fixture[0]


@pytest.mark.django_db
def test_race_creation(race_fixture, size_fixture, source_fixture):
    race = race_fixture[0]
    assert race.name == "Human"
    assert race.description == "Sum desc"
    assert race.link == "https://www.human.com"
    assert race.level_adjustment == 0
    assert race.size == size_fixture[1]
    assert race.source == source_fixture[0]


@pytest.mark.django_db
def test_race_type_creation(race_type_fixture, race_fixture, character_type_fixture):
    race_type = race_type_fixture[0]
    assert race_type.race == race_fixture[0]
    assert race_type.character_type == character_type_fixture[0]


@pytest.mark.django_db
def test_race_ability_modifier_creation(
    race_ability_modifier_fixture, race_fixture, ability_modifier_fixture
):
    race_ability_modifier = race_ability_modifier_fixture[0]
    assert race_ability_modifier.race == race_fixture[0]
    assert race_ability_modifier.ability_modifier == ability_modifier_fixture[0]


@pytest.mark.django_db
def test_race_trait_creation(race_trait_fixture, race_fixture, trait_fixture):
    race_trait = race_trait_fixture[0]
    assert race_trait.race == race_fixture[0]
    assert race_trait.trait == trait_fixture[0]
    assert race_trait.additional_value == "Some value"


@pytest.mark.django_db
def test_race_language_creation(race_language_fixture, race_fixture, language_fixture):
    race_language = race_language_fixture[0]
    assert race_language.race == race_fixture[0]
    assert race_language.language == language_fixture[0]
    assert race_language.is_automatic is True


@pytest.mark.django_db
def test_race_favored_class_creation(
    race_favored_class_fixture, race_fixture, character_class_fixture
):
    race_favored_class = race_favored_class_fixture[0]
    assert race_favored_class.race == race_fixture[0]
    assert race_favored_class.character_class == character_class_fixture[0]
