import pytest

from character_class.models import (
    BSBProgression,
    BABProgression,
    CharacterClass,
    ClassAlignment,
    ClassSkill,
    ClassBsbProgression,
    ClassBonusLanguage,
    PrestigeCharacterClass,
    PrestigeClassSkillRankRequirement,
    PrestigeClassLanguageRequirement,
    PrestigeClassFeatRequirement,
)


@pytest.fixture()
def bsb_progression_fixture(ability_fixture):
    return BSBProgression.objects.bulk_create(
        [
            BSBProgression(
                name="Fortitude (Good)",
                save_bonus_table={
                    "1": 2,
                    "2": 3,
                    "3": 3,
                    "4": 4,
                    "5": 4,
                    "6": 5,
                    "7": 5,
                },
                ability=ability_fixture[0],
            ),
            BSBProgression(
                name="Fortitude (Poor)",
                save_bonus_table={
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 1,
                    "5": 1,
                    "6": 2,
                    "7": 2,
                },
                ability=ability_fixture[1],
            ),
            BSBProgression(
                name="Fortitude (Medium)",
                save_bonus_table={
                    "1": 2,
                    "2": 3,
                    "3": 3,
                    "4": 4,
                    "5": 4,
                    "6": 5,
                    "7": 5,
                },
                ability=ability_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def bab_progression_fixture(ability_fixture):
    return BABProgression.objects.bulk_create(
        [
            BABProgression(
                name="Good",
                attack_bonus_table={
                    "1": 2,
                    "2": 3,
                    "3": 3,
                    "4": 4,
                    "5": 4,
                    "6": 5,
                    "7": 5,
                },
            ),
            BABProgression(
                name="Poor",
                attack_bonus_table={
                    "1": 0,
                    "2": 0,
                    "3": 1,
                    "4": 1,
                    "5": 1,
                    "6": 2,
                    "7": 2,
                },
            ),
            BABProgression(
                name="Medium",
                attack_bonus_table={
                    "1": 2,
                    "2": 3,
                    "3": 3,
                    "4": 4,
                    "5": 5,
                    "6": 6,
                    "7": 7,
                },
            ),
        ]
    )


@pytest.fixture()
def character_class_fixture(
    source_fixture, die_fixture, bab_progression_fixture, bsb_progression_fixture
):
    return CharacterClass.objects.bulk_create(
        [
            CharacterClass(
                name="Fighter",
                description="Desc here",
                max_level=20,
                link="https://fighterinio.com",
                skill_points_per_level=4,
                spells_per_day={
                    "level 1": {"0": "3", "1": "1+1"},
                    "level 2": {"0": "4", "1": "2+1"},
                    "level 3": {"0": "4", "1": "2+1", "2": "1+1"},
                },
                source=source_fixture[0],
                hit_die=die_fixture[1],
                bab_progression=bab_progression_fixture[0],
            ),
            CharacterClass(
                name="Slacker",
                max_level=20,
                skill_points_per_level=4,
                hit_die=die_fixture[1],
                bab_progression=bab_progression_fixture[1],
            ),
            CharacterClass(
                name="Grog",
                max_level=10,
                skill_points_per_level=8,
                hit_die=die_fixture[1],
                bab_progression=bab_progression_fixture[2],
            ),
        ]
    )


@pytest.fixture()
def class_alignment_fixture(character_class_fixture, alignment_fixture):
    return [
        ClassAlignment.objects.create(
            character_class=character_class_fixture[0], alignment=alignment_fixture[0]
        ),
        ClassAlignment.objects.create(
            character_class=character_class_fixture[0], alignment=alignment_fixture[1]
        ),
        ClassAlignment.objects.create(
            character_class=character_class_fixture[1], alignment=alignment_fixture[1]
        ),
    ]


@pytest.fixture()
def class_skill_fixture(character_class_fixture, skill_fixture):
    return [
        ClassSkill.objects.create(
            character_class=character_class_fixture[0], skill=skill_fixture[0]
        ),
        ClassSkill.objects.create(
            character_class=character_class_fixture[0], skill=skill_fixture[1]
        ),
        ClassSkill.objects.create(
            character_class=character_class_fixture[1], skill=skill_fixture[0]
        ),
        ClassSkill.objects.create(
            character_class=character_class_fixture[2], skill=skill_fixture[0]
        ),
    ]


@pytest.fixture()
def class_bsb_progression_fixture(character_class_fixture, bsb_progression_fixture):
    return [
        ClassBsbProgression.objects.create(
            character_class=character_class_fixture[0],
            bsb_progression=bsb_progression_fixture[0],
        ),
        ClassBsbProgression.objects.create(
            character_class=character_class_fixture[0],
            bsb_progression=bsb_progression_fixture[1],
        ),
        ClassBsbProgression.objects.create(
            character_class=character_class_fixture[1],
            bsb_progression=bsb_progression_fixture[1],
        ),
        ClassBsbProgression.objects.create(
            character_class=character_class_fixture[2],
            bsb_progression=bsb_progression_fixture[2],
        ),
    ]


@pytest.fixture()
def class_bonus_language_fixture(character_class_fixture, language_fixture):
    return [
        ClassBonusLanguage.objects.create(
            character_class=character_class_fixture[0], language=language_fixture[0]
        ),
        ClassBonusLanguage.objects.create(
            character_class=character_class_fixture[1], language=language_fixture[1]
        ),
        ClassBonusLanguage.objects.create(
            character_class=character_class_fixture[2], language=language_fixture[1]
        ),
    ]


@pytest.fixture()
def prestige_class_fixture(
    source_fixture, die_fixture, bab_progression_fixture, bsb_progression_fixture
):
    return [
        PrestigeCharacterClass.objects.create(
            name="Grog",
            max_level=10,
            skill_points_per_level=8,
            hit_die=die_fixture[2],
            bab_progression=bab_progression_fixture[2],
            required_bab=5,
        ),
        PrestigeCharacterClass.objects.create(
            name="ssss",
            max_level=10,
            skill_points_per_level=8,
            hit_die=die_fixture[2],
            bab_progression=bab_progression_fixture[1],
            required_bab=12,
        ),
    ]


@pytest.fixture()
def prestige_class_skill_rank_requirement_fixture(
    prestige_class_fixture, skill_fixture
):
    return [
        PrestigeClassSkillRankRequirement.objects.create(
            prestige_class=prestige_class_fixture[0],
            skill=skill_fixture[0],
            required_ranks=5,
        ),
        PrestigeClassSkillRankRequirement.objects.create(
            prestige_class=prestige_class_fixture[0],
            skill=skill_fixture[1],
            required_ranks=10,
        ),
        PrestigeClassSkillRankRequirement.objects.create(
            prestige_class=prestige_class_fixture[1],
            skill=skill_fixture[1],
            required_ranks=10,
        ),
    ]


@pytest.fixture()
def prestige_class_language_requirement_fixture(
    prestige_class_fixture, language_fixture
):
    return [
        PrestigeClassLanguageRequirement.objects.create(
            prestige_class=prestige_class_fixture[0], language=language_fixture[0]
        ),
        PrestigeClassLanguageRequirement.objects.create(
            prestige_class=prestige_class_fixture[0], language=language_fixture[1]
        ),
        PrestigeClassLanguageRequirement.objects.create(
            prestige_class=prestige_class_fixture[1], language=language_fixture[1]
        ),
    ]


@pytest.fixture()
def prestige_class_feat_requirement_fixture(prestige_class_fixture, feat_fixture):
    return [
        PrestigeClassFeatRequirement.objects.create(
            prestige_class=prestige_class_fixture[0], feat=feat_fixture[0]
        ),
        PrestigeClassFeatRequirement.objects.create(
            prestige_class=prestige_class_fixture[0], feat=feat_fixture[1]
        ),
        PrestigeClassFeatRequirement.objects.create(
            prestige_class=prestige_class_fixture[1], feat=feat_fixture[2]
        ),
    ]
