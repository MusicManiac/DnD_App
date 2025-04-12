import pytest


@pytest.mark.django_db
def test_bsb_progression_creation(bsb_progression_fixture, ability_fixture):
    bsb_progression = bsb_progression_fixture[0]
    assert bsb_progression.name == "Fortitude (Good)"
    assert bsb_progression.save_bonus_table == {
        "1": 2,
        "2": 3,
        "3": 3,
        "4": 4,
        "5": 4,
        "6": 5,
        "7": 5,
    }
    assert bsb_progression.ability == ability_fixture[0]


@pytest.mark.django_db
def test_bab_progression_creation(bab_progression_fixture, ability_fixture):
    bab_progression = bab_progression_fixture[0]
    assert bab_progression.name == "Good"
    assert bab_progression.attack_bonus_table == {
        "1": 2,
        "2": 3,
        "3": 3,
        "4": 4,
        "5": 4,
        "6": 5,
        "7": 5,
    }


@pytest.mark.django_db
def test_character_class_creation(
    character_class_fixture, source_fixture, die_fixture, bab_progression_fixture
):
    character_class = character_class_fixture[0]
    assert character_class.name == "Fighter"
    assert character_class.description == "Desc here"
    assert character_class.max_level == 20
    assert character_class.link == "https://fighterinio.com"
    assert character_class.skill_points_per_level == 4
    assert character_class.spells_per_day == {
        "level 1": {"0": "3", "1": "1+1"},
        "level 2": {"0": "4", "1": "2+1"},
        "level 3": {"0": "4", "1": "2+1", "2": "1+1"},
    }
    assert character_class.source == source_fixture[0]
    assert character_class.hit_die == die_fixture[1]
    assert character_class.bab_progression == bab_progression_fixture[0]


@pytest.mark.django_db
def test_class_alignment_creation(
    class_alignment_fixture, character_class_fixture, alignment_fixture
):
    class_alignment = class_alignment_fixture[0]
    assert class_alignment.character_class == character_class_fixture[0]
    assert class_alignment.alignment == alignment_fixture[0]


@pytest.mark.django_db
def test_class_skill_creation(
    class_skill_fixture, character_class_fixture, skill_fixture
):
    class_skill = class_skill_fixture[0]
    assert class_skill.character_class == character_class_fixture[0]
    assert class_skill.skill == skill_fixture[0]


@pytest.mark.django_db
def test_class_bsb_progression_creation(
    class_bsb_progression_fixture, character_class_fixture, bsb_progression_fixture
):
    class_bsb_progression = class_bsb_progression_fixture[0]
    assert class_bsb_progression.character_class == character_class_fixture[0]
    assert class_bsb_progression.bsb_progression == bsb_progression_fixture[0]


@pytest.mark.django_db
def test_class_bonus_language_creation(
    class_bonus_language_fixture, character_class_fixture, language_fixture
):
    class_bonus_language = class_bonus_language_fixture[0]
    assert class_bonus_language.character_class == character_class_fixture[0]
    assert class_bonus_language.language == language_fixture[0]


@pytest.mark.django_db
def test_prestige_class_creation(
    prestige_class_fixture, source_fixture, die_fixture, bab_progression_fixture
):
    prestige_class = prestige_class_fixture[0]
    assert prestige_class.name == "Grog"
    assert prestige_class.max_level == 10
    assert prestige_class.skill_points_per_level == 8
    assert prestige_class.hit_die == die_fixture[2]
    assert prestige_class.bab_progression == bab_progression_fixture[2]
    assert prestige_class.required_bab == 5


@pytest.mark.django_db
def test_prestige_class_skill_rank_requirement_creation(
    prestige_class_skill_rank_requirement_fixture, prestige_class_fixture, skill_fixture
):
    skill_rank_requirement = prestige_class_skill_rank_requirement_fixture[0]
    assert skill_rank_requirement.prestige_class == prestige_class_fixture[0]
    assert skill_rank_requirement.skill == skill_fixture[0]
    assert skill_rank_requirement.required_ranks == 5


@pytest.mark.django_db
def test_prestige_class_language_requirement_creation(
    prestige_class_language_requirement_fixture,
    prestige_class_fixture,
    language_fixture,
):
    language_requirement = prestige_class_language_requirement_fixture[0]
    assert language_requirement.prestige_class == prestige_class_fixture[0]
    assert language_requirement.language == language_fixture[0]


@pytest.mark.django_db
def test_prestige_class_feat_requirement_creation(
    prestige_class_feat_requirement_fixture, prestige_class_fixture, feat_fixture
):
    feat_requirement = prestige_class_feat_requirement_fixture[0]
    assert feat_requirement.prestige_class == prestige_class_fixture[0]
    assert feat_requirement.feat == feat_fixture[0]
