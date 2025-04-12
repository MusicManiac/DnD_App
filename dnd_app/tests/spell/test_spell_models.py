import pytest


@pytest.mark.django_db
def test_magic_aura_strength_creation(magic_aura_strength_fixture):
    magic_aura_strength = magic_aura_strength_fixture[0]
    assert magic_aura_strength.name == "Weak"
    assert magic_aura_strength.description == "Weak magic aura"
    assert str(magic_aura_strength) == "Weak"


@pytest.mark.django_db
def test_magic_school_fixture(magic_school_fixture):
    magic_school = magic_school_fixture[0]
    assert magic_school.name == "Abjuration"
    assert magic_school.description == "Abjuration magic"


@pytest.mark.django_db
def test_magic_subschool_fixture(magic_subschool_fixture):
    magic_subschool = magic_subschool_fixture[0]
    assert magic_subschool.name == "Teleportation"
    assert magic_subschool.description == "Teleportation magic"


@pytest.mark.django_db
def test_spell_descriptor_fixture(spell_descriptor_fixture):
    spell_descriptor = spell_descriptor_fixture[0]
    assert spell_descriptor.name == "Fire"
    assert spell_descriptor.description == "Fire magic"


@pytest.mark.django_db
def test_spell_component_fixture(spell_component_fixture):
    spell_component = spell_component_fixture[0]
    assert spell_component.name == "Verbal"
    assert spell_component.short_name == "V"
    assert spell_component.description == "Verbal component"


@pytest.mark.django_db
def test_casting_time_fixture(casting_time_fixture):
    casting_time = casting_time_fixture[0]
    assert casting_time.name == "Standard"
    assert casting_time.description == "Standard casting time"


@pytest.mark.django_db
def test_spell_range_fixture(spell_range_fixture):
    spell_range = spell_range_fixture[0]
    assert spell_range.name == "Close"
    assert spell_range.description == "Close range"


@pytest.mark.django_db
def test_spell_fixture(
    magic_school_fixture,
    magic_subschool_fixture,
    casting_time_fixture,
    spell_range_fixture,
    spell_fixture,
):
    spell = spell_fixture[0]
    assert spell.name == "Fireball"
    assert spell.description == "BIG BALL OF FOIRE"
    assert spell.link == "https://www.fireball.com"
    assert spell.target == "Point in space"
    assert spell.effect == "Big boom"
    assert spell.area == "20 ft radius"
    assert spell.duration == "Instantaneous"
    assert spell.saving_throw == "Dexterity"
    assert spell.spell_resistance is True
    assert spell.school == magic_school_fixture[0]
    assert spell.subschool == magic_subschool_fixture[0]
    assert spell.casting_time == casting_time_fixture[0]
    assert spell.range == spell_range_fixture[0]


@pytest.mark.django_db
def test_spell_spell_descriptor_fixture(
    spell_spell_descriptor_fixture, spell_descriptor_fixture, spell_fixture
):
    ssd = spell_spell_descriptor_fixture[0]
    assert ssd.spell == spell_fixture[0]
    assert ssd.descriptor == spell_descriptor_fixture[0]


@pytest.mark.django_db
def test_spell_level_fixture(
    spell_fixture, character_class_fixture, spell_level_fixture
):
    spell_level = spell_level_fixture[0]
    assert spell_level.spell == spell_fixture[0]
    assert spell_level.character_class == character_class_fixture[0]
    assert spell_level.level == 3


@pytest.mark.django_db
def test_spell_spell_component_fixture(
    spell_spell_component_fixture, spell_component_fixture, spell_fixture
):
    ssc = spell_spell_component_fixture[0]
    assert ssc.spell == spell_fixture[0]
    assert ssc.component == spell_component_fixture[0]
