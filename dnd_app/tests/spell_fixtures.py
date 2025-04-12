import pytest

from spell.models import (
    MagicAuraStrength,
    MagicSchool,
    MagicSubSchool,
    SpellDescriptor,
    SpellComponent,
    CastingTime,
    SpellRange,
    Spell,
    SpellSpellDescriptor,
    SpellLevel,
    SpellSpellComponent,
)


@pytest.fixture()
def magic_aura_strength_fixture():
    return MagicAuraStrength.objects.bulk_create(
        [
            MagicAuraStrength(name="Weak", description="Weak magic aura"),
            MagicAuraStrength(name="Moderate", description="Moderate magic aura"),
            MagicAuraStrength(name="Strong", description="Strong magic aura"),
        ]
    )


@pytest.fixture()
def magic_school_fixture():
    return MagicSchool.objects.bulk_create(
        [
            MagicSchool(name="Abjuration", description="Abjuration magic"),
            MagicSchool(name="Conjuration", description="Conjuration magic"),
            MagicSchool(name="Divination", description="Divination magic"),
        ]
    )


@pytest.fixture()
def magic_subschool_fixture():
    return [
        MagicSubSchool.objects.create(
            name="Teleportation", description="Teleportation magic"
        ),
        MagicSubSchool.objects.create(name="Summoning", description="Summoning magic"),
        MagicSubSchool.objects.create(name="Divining", description="Divining magic"),
    ]


@pytest.fixture()
def spell_descriptor_fixture():
    return SpellDescriptor.objects.bulk_create(
        [
            SpellDescriptor(name="Fire", description="Fire magic"),
            SpellDescriptor(name="Ice", description="Ice magic"),
            SpellDescriptor(name="Lightning", description="Lightning magic"),
        ]
    )


@pytest.fixture()
def spell_component_fixture():
    return SpellComponent.objects.bulk_create(
        [
            SpellComponent(
                name="Verbal", short_name="V", description="Verbal component"
            ),
            SpellComponent(
                name="Somatic", short_name="S", description="Somatic component"
            ),
            SpellComponent(
                name="Material", short_name="M", description="Material component"
            ),
        ]
    )


@pytest.fixture()
def casting_time_fixture():
    return CastingTime.objects.bulk_create(
        [
            CastingTime(name="Standard", description="Standard casting time"),
            CastingTime(name="Full", description="Full casting time"),
            CastingTime(name="Swift", description="Swift casting time"),
        ]
    )


@pytest.fixture()
def spell_range_fixture():
    return SpellRange.objects.bulk_create(
        [
            SpellRange(name="Close", description="Close range"),
            SpellRange(name="Medium", description="Medium range"),
            SpellRange(name="Long", description="Long range"),
        ]
    )


@pytest.fixture()
def spell_fixture(
    magic_school_fixture,
    magic_subschool_fixture,
    casting_time_fixture,
    spell_range_fixture,
):
    return Spell.objects.bulk_create(
        [
            Spell(
                name="Fireball",
                description="BIG BALL OF FOIRE",
                link="https://www.fireball.com",
                target="Point in space",
                effect="Big boom",
                area="20 ft radius",
                duration="Instantaneous",
                saving_throw="Dexterity",
                spell_resistance=True,
                school=magic_school_fixture[0],
                subschool=magic_subschool_fixture[0],
                casting_time=casting_time_fixture[0],
                range=spell_range_fixture[0],
            ),
            Spell(
                name="Lightning Bolt",
                description="ZAP ZAP ZAP",
                school=magic_school_fixture[1],
                casting_time=casting_time_fixture[1],
                range=spell_range_fixture[1],
            ),
            Spell(
                name="Ice Storm",
                description="GET FROZEN NERD",
                school=magic_school_fixture[1],
                casting_time=casting_time_fixture[1],
                range=spell_range_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def spell_spell_descriptor_fixture(spell_fixture, spell_descriptor_fixture):
    return [
        SpellSpellDescriptor.objects.create(
            spell=spell_fixture[0], descriptor=spell_descriptor_fixture[0]
        ),
        SpellSpellDescriptor.objects.create(
            spell=spell_fixture[1], descriptor=spell_descriptor_fixture[1]
        ),
        SpellSpellDescriptor.objects.create(
            spell=spell_fixture[1], descriptor=spell_descriptor_fixture[2]
        ),
    ]


@pytest.fixture()
def spell_level_fixture(spell_fixture, character_class_fixture):
    return [
        SpellLevel.objects.create(
            spell=spell_fixture[0], character_class=character_class_fixture[0], level=3
        ),
        SpellLevel.objects.create(
            spell=spell_fixture[1], character_class=character_class_fixture[1], level=5
        ),
        SpellLevel.objects.create(
            spell=spell_fixture[2], character_class=character_class_fixture[2], level=7
        ),
    ]


@pytest.fixture()
def spell_spell_component_fixture(spell_fixture, spell_component_fixture):
    return [
        SpellSpellComponent.objects.create(
            spell=spell_fixture[0], component=spell_component_fixture[0]
        ),
        SpellSpellComponent.objects.create(
            spell=spell_fixture[1], component=spell_component_fixture[1]
        ),
        SpellSpellComponent.objects.create(
            spell=spell_fixture[2], component=spell_component_fixture[2]
        ),
    ]
