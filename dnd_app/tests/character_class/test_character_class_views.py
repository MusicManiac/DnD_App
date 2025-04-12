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
)
from race.models import RaceFavoredClass


@pytest.mark.django_db
def test_bsb_progression_list_view(client, bsb_progression_fixture):
    response = client.get("/api/character_class/bsb_progression/")

    assert response.status_code == 200
    assert len(response.data) == len(bsb_progression_fixture)
    assert {progression["name"] for progression in response.data} == {
        progression.name for progression in bsb_progression_fixture
    }


@pytest.mark.django_db
def test_bsb_progression_create_view_success(client, ability_fixture):
    data = {
        "name": "Reflex (Good)",
        "save_bonus_table": {
            "1": 2,
            "2": 3,
            "3": 4,
            "4": 5,
            "5": 6,
            "6": 7,
            "7": 8,
        },
        "ability": ability_fixture[0].id,
    }

    response = client.post("/api/character_class/bsb_progression/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Reflex (Good)"
    assert response.data["save_bonus_table"] == {
        "1": 2,
        "2": 3,
        "3": 4,
        "4": 5,
        "5": 6,
        "6": 7,
        "7": 8,
    }
    assert response.data["ability"] == ability_fixture[0].id


@pytest.mark.django_db
def test_bsb_progression_create_view_fail(
    client, bsb_progression_fixture, ability_fixture
):
    pass


@pytest.mark.django_db
def test_bsb_progression_edit_view(client, bsb_progression_fixture):
    progression = bsb_progression_fixture[0]
    updated_data = {
        "name": "Fortitude (Updated)",
        "save_bonus_table": {
            "1": 2,
            "2": 3,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
        },
        "ability": progression.ability.id,
    }

    response = client.put(
        f"/api/character_class/bsb_progression/{progression.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Fortitude (Updated)"
    assert response.data["save_bonus_table"] == {
        "1": 2,
        "2": 3,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
    }


@pytest.mark.django_db
def test_bsb_progression_delete_view(client, bsb_progression_fixture):
    progression = bsb_progression_fixture[0]

    response = client.delete(f"/api/character_class/bsb_progression/{progression.id}/")

    assert response.status_code == 204
    assert not BSBProgression.objects.filter(id=progression.id).exists()


@pytest.mark.django_db
def test_bab_progression_list_view(client, bab_progression_fixture):
    response = client.get("/api/character_class/bab_progression/")

    assert response.status_code == 200
    assert len(response.data) == len(bab_progression_fixture)
    assert {progression["name"] for progression in response.data} == {
        progression.name for progression in bab_progression_fixture
    }


@pytest.mark.django_db
def test_bab_progression_create_view_success(client):
    data = {
        "name": "Excellent",
        "attack_bonus_table": {
            "1": 3,
            "2": 4,
            "3": 5,
            "4": 6,
            "5": 7,
            "6": 8,
            "7": 9,
        },
    }

    response = client.post("/api/character_class/bab_progression/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Excellent"
    assert response.data["attack_bonus_table"] == {
        "1": 3,
        "2": 4,
        "3": 5,
        "4": 6,
        "5": 7,
        "6": 8,
        "7": 9,
    }


@pytest.mark.django_db
def test_bab_progression_create_view_fail(client, bab_progression_fixture):
    pass


@pytest.mark.django_db
def test_bab_progression_edit_view(client, bab_progression_fixture):
    progression = bab_progression_fixture[0]
    updated_data = {
        "name": "Good (Updated)",
        "attack_bonus_table": {
            "1": 2,
            "2": 3,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 6,
        },
    }

    response = client.put(
        f"/api/character_class/bab_progression/{progression.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Good (Updated)"
    assert response.data["attack_bonus_table"] == {
        "1": 2,
        "2": 3,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 6,
    }


@pytest.mark.django_db
def test_bab_progression_delete_view(client, bab_progression_fixture):
    progression = bab_progression_fixture[0]

    response = client.delete(f"/api/character_class/bab_progression/{progression.id}/")

    assert response.status_code == 204
    assert not BABProgression.objects.filter(id=progression.id).exists()


@pytest.mark.django_db
def test_character_class_list_view(client, character_class_fixture):
    response = client.get("/api/character_class/character_classes/")

    assert response.status_code == 200
    assert len(response.data) == len(character_class_fixture)
    assert {char_class["name"] for char_class in response.data} == {
        char_class.name for char_class in character_class_fixture
    }


@pytest.mark.django_db
def test_character_class_create_view_success(
    client, source_fixture, die_fixture, bab_progression_fixture
):
    data = {
        "name": "Mage",
        "description": "A master of spells.",
        "max_level": 20,
        "link": "https://mage.com",
        "skill_points_per_level": 4,
        "spells_per_day": {
            "level 1": {"0": "3", "1": "1+1"},
            "level 2": {"0": "4", "1": "2+1"},
            "level 3": {"0": "4", "1": "2+1", "2": "1+1"},
        },
        "source": source_fixture[0].id,
        "hit_die": die_fixture[1].id,
        "bab_progression": bab_progression_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/character_classes/", data, format="json"
    )

    assert response.status_code == 201
    assert response.data["name"] == "Mage"
    assert response.data["description"] == "A master of spells."
    assert response.data["skill_points_per_level"] == 4
    assert response.data["spells_per_day"] == {
        "level 1": {"0": "3", "1": "1+1"},
        "level 2": {"0": "4", "1": "2+1"},
        "level 3": {"0": "4", "1": "2+1", "2": "1+1"},
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_errors",
    [
        (
            {
                "name": "Fighter",
                "max_level": 20,
                "skill_points_per_level": 4,
                "hit_die": 1,
                "bab_progression": 1,
            },
            {"name": ["character class with this name already exists."]},
        ),
        (
            {},
            {
                "name": ["This field is required."],
                "hit_die": ["This field is required."],
                "bab_progression": ["This field is required."],
            },
        ),
    ],
)
def test_character_class_create_view_fail(
    client,
    data,
    expected_errors,
    character_class_fixture,
    die_fixture,
    bab_progression_fixture,
):
    response = client.post(
        "/api/character_class/character_classes/", data, format="json"
    )
    assert response.status_code == 400

    for field, error_messages in expected_errors.items():
        assert field in response.data
        for error_message in error_messages:
            assert error_message in response.data[field]


@pytest.mark.django_db
def test_character_class_edit_view(
    client, character_class_fixture, die_fixture, bab_progression_fixture
):
    char_class = character_class_fixture[0]
    updated_data = {
        "name": "Updated Fighter",
        "description": "Updated description",
        "max_level": 15,
        "skill_points_per_level": 5,
        "hit_die": die_fixture[1].id,
        "bab_progression": bab_progression_fixture[1].id,
    }

    response = client.put(
        f"/api/character_class/character_classes/{char_class.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Fighter"
    assert response.data["description"] == "Updated description"
    assert response.data["max_level"] == 15
    assert response.data["skill_points_per_level"] == 5


@pytest.mark.django_db
def test_character_class_delete_view_success(client, character_class_fixture):
    char_class = character_class_fixture[0]

    response = client.delete(f"/api/character_class/character_classes/{char_class.id}/")

    assert response.status_code == 204
    assert not CharacterClass.objects.filter(id=char_class.id).exists()


@pytest.mark.django_db
def test_character_class_delete_view_fail(
    client,
    character_class_fixture,
    class_alignment_fixture,
    class_skill_fixture,
    class_bsb_progression_fixture,
    class_bonus_language_fixture,
    race_favored_class_fixture,
):
    char_class = character_class_fixture[0]
    # Check all character class M2M relationships
    assert ClassAlignment.objects.filter(character_class=char_class).exists()
    assert ClassSkill.objects.filter(character_class=char_class).exists()
    assert ClassBsbProgression.objects.filter(character_class=char_class).exists()
    assert ClassBonusLanguage.objects.filter(character_class=char_class).exists()
    # Check that there's a dependand object
    assert RaceFavoredClass.objects.filter(character_class=char_class).exists()

    response = client.delete(f"/api/character_class/character_classes/{char_class.id}/")

    assert response.status_code == 400
    assert "detail" in response.data
    assert (
        "This object cannot be deleted because it has dependent objects."
        in response.data["detail"]
    )
    # Nothing is deleted
    assert CharacterClass.objects.filter(id=char_class.id).exists()
    assert ClassAlignment.objects.filter(character_class=char_class).exists()
    assert ClassSkill.objects.filter(character_class=char_class).exists()
    assert ClassBsbProgression.objects.filter(character_class=char_class).exists()
    assert ClassBonusLanguage.objects.filter(character_class=char_class).exists()


@pytest.mark.django_db
def test_class_alignment_list_view(client, class_alignment_fixture):
    response = client.get("/api/character_class/class_alignments/")

    assert response.status_code == 200
    assert len(response.data) == len(class_alignment_fixture)
    assert {ca["character_class"] for ca in response.data} == {
        ca.character_class.id for ca in class_alignment_fixture
    }
    assert {ca["alignment"] for ca in response.data} == {
        ca.alignment.id for ca in class_alignment_fixture
    }


@pytest.mark.django_db
def test_class_alignment_create_view_success(
    client, character_class_fixture, alignment_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "alignment": alignment_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/class_alignments/", data, format="json"
    )

    assert response.status_code == 201
    assert response.data["character_class"] == character_class_fixture[0].id
    assert response.data["alignment"] == alignment_fixture[0].id


@pytest.mark.django_db
def test_class_alignment_create_view_fail(
    client, class_alignment_fixture, character_class_fixture, alignment_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "alignment": alignment_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/class_alignments/", data, format="json"
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields character_class, alignment must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_class_alignment_edit_view(client, class_alignment_fixture):
    class_alignment = class_alignment_fixture[0]
    updated_data = {
        "character_class": class_alignment.character_class.id,
        "alignment": class_alignment.alignment.id,
    }

    response = client.put(
        f"/api/character_class/class_alignments/{class_alignment.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["character_class"] == class_alignment.character_class.id
    assert response.data["alignment"] == class_alignment.alignment.id


@pytest.mark.django_db
def test_class_alignment_delete_view(client, class_alignment_fixture):
    class_alignment = class_alignment_fixture[0]

    response = client.delete(
        f"/api/character_class/class_alignments/{class_alignment.id}/"
    )

    assert response.status_code == 204
    assert not ClassAlignment.objects.filter(id=class_alignment.id).exists()


@pytest.mark.django_db
def test_class_skill_list_view(client, class_skill_fixture):
    response = client.get("/api/character_class/class_skills/")

    assert response.status_code == 200
    assert len(response.data) == len(class_skill_fixture)
    assert {cs["character_class"] for cs in response.data} == {
        cs.character_class.id for cs in class_skill_fixture
    }
    assert {cs["skill"] for cs in response.data} == {
        cs.skill.id for cs in class_skill_fixture
    }


@pytest.mark.django_db
def test_class_skill_create_view_success(
    client, character_class_fixture, skill_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "skill": skill_fixture[0].id,
    }

    response = client.post("/api/character_class/class_skills/", data, format="json")

    assert response.status_code == 201
    assert response.data["character_class"] == character_class_fixture[0].id
    assert response.data["skill"] == skill_fixture[0].id


@pytest.mark.django_db
def test_class_skill_create_view_fail(
    client, class_skill_fixture, character_class_fixture, skill_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "skill": skill_fixture[0].id,
    }

    response = client.post("/api/character_class/class_skills/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields character_class, skill must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_class_skill_edit_view(client, class_skill_fixture):
    class_skill = class_skill_fixture[0]
    updated_data = {
        "character_class": class_skill.character_class.id,
        "skill": class_skill.skill.id,
    }

    response = client.put(
        f"/api/character_class/class_skills/{class_skill.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["character_class"] == class_skill.character_class.id
    assert response.data["skill"] == class_skill.skill.id


@pytest.mark.django_db
def test_class_skill_delete_view(client, class_skill_fixture):
    class_skill = class_skill_fixture[0]

    response = client.delete(f"/api/character_class/class_skills/{class_skill.id}/")

    assert response.status_code == 204
    assert not ClassSkill.objects.filter(id=class_skill.id).exists()


@pytest.mark.django_db
def test_class_bsb_progression_list_view(client, class_bsb_progression_fixture):
    response = client.get("/api/character_class/class_bsb_progressions/")

    assert response.status_code == 200
    assert len(response.data) == len(class_bsb_progression_fixture)
    assert {cbp["character_class"] for cbp in response.data} == {
        cbp.character_class.id for cbp in class_bsb_progression_fixture
    }
    assert {cbp["bsb_progression"] for cbp in response.data} == {
        cbp.bsb_progression.id for cbp in class_bsb_progression_fixture
    }


@pytest.mark.django_db
def test_class_bsb_progression_create_view_success(
    client, character_class_fixture, bsb_progression_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "bsb_progression": bsb_progression_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/class_bsb_progressions/", data, format="json"
    )

    assert response.status_code == 201
    assert response.data["character_class"] == character_class_fixture[0].id
    assert response.data["bsb_progression"] == bsb_progression_fixture[0].id


@pytest.mark.django_db
def test_class_bsb_progression_create_view_fail(
    client,
    class_bsb_progression_fixture,
    character_class_fixture,
    bsb_progression_fixture,
):
    data = {
        "character_class": character_class_fixture[0].id,
        "bsb_progression": bsb_progression_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/class_bsb_progressions/", data, format="json"
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields character_class, bsb_progression must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_class_bsb_progression_edit_view(client, class_bsb_progression_fixture):
    class_bsb_progression = class_bsb_progression_fixture[0]
    updated_data = {
        "character_class": class_bsb_progression.character_class.id,
        "bsb_progression": class_bsb_progression.bsb_progression.id,
    }

    response = client.put(
        f"/api/character_class/class_bsb_progressions/{class_bsb_progression.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["character_class"] == class_bsb_progression.character_class.id
    assert response.data["bsb_progression"] == class_bsb_progression.bsb_progression.id


@pytest.mark.django_db
def test_class_bsb_progression_delete_view(client, class_bsb_progression_fixture):
    class_bsb_progression = class_bsb_progression_fixture[0]

    response = client.delete(
        f"/api/character_class/class_bsb_progressions/{class_bsb_progression.id}/"
    )

    assert response.status_code == 204
    assert not ClassBsbProgression.objects.filter(id=class_bsb_progression.id).exists()


@pytest.mark.django_db
def test_class_bonus_language_list_view(client, class_bonus_language_fixture):
    response = client.get("/api/character_class/class_bonus_languages/")

    assert response.status_code == 200
    assert len(response.data) == len(class_bonus_language_fixture)
    assert {cbl["character_class"] for cbl in response.data} == {
        cbl.character_class.id for cbl in class_bonus_language_fixture
    }
    assert {cbl["language"] for cbl in response.data} == {
        cbl.language.id for cbl in class_bonus_language_fixture
    }


@pytest.mark.django_db
def test_class_bonus_language_create_view_success(
    client, character_class_fixture, language_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "language": language_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/class_bonus_languages/", data, format="json"
    )

    assert response.status_code == 201
    assert response.data["character_class"] == character_class_fixture[0].id
    assert response.data["language"] == language_fixture[0].id


@pytest.mark.django_db
def test_class_bonus_language_create_view_fail(
    client, class_bonus_language_fixture, character_class_fixture, language_fixture
):
    data = {
        "character_class": character_class_fixture[0].id,
        "language": language_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/class_bonus_languages/", data, format="json"
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields character_class, language must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_class_bonus_language_edit_view(client, class_bonus_language_fixture):
    class_bonus_language = class_bonus_language_fixture[0]
    updated_data = {
        "character_class": class_bonus_language.character_class.id,
        "language": class_bonus_language.language.id,
    }

    response = client.put(
        f"/api/character_class/class_bonus_languages/{class_bonus_language.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["character_class"] == class_bonus_language.character_class.id
    assert response.data["language"] == class_bonus_language.language.id


@pytest.mark.django_db
def test_class_bonus_language_delete_view(client, class_bonus_language_fixture):
    class_bonus_language = class_bonus_language_fixture[0]

    response = client.delete(
        f"/api/character_class/class_bonus_languages/{class_bonus_language.id}/"
    )

    assert response.status_code == 204
    assert not ClassBonusLanguage.objects.filter(id=class_bonus_language.id).exists()


@pytest.mark.django_db
def test_prestige_character_class_list_view(client, prestige_class_fixture):
    response = client.get("/api/character_class/prestige_character_classes/")

    assert response.status_code == 200
    assert len(response.data) == len(prestige_class_fixture)
    assert {prestige_class["name"] for prestige_class in response.data} == {
        prestige_class.name for prestige_class in prestige_class_fixture
    }


@pytest.mark.django_db
def test_prestige_character_class_create_view_success(
    client, die_fixture, bab_progression_fixture
):
    data = {
        "name": "Master Fighter",
        "max_level": 10,
        "skill_points_per_level": 8,
        "hit_die": die_fixture[2].id,
        "bab_progression": bab_progression_fixture[1].id,
        "required_bab": 6,
    }

    response = client.post(
        "/api/character_class/prestige_character_classes/", data, format="json"
    )

    assert response.status_code == 201
    assert response.data["name"] == "Master Fighter"
    assert response.data["max_level"] == 10
    assert response.data["required_bab"] == 6


@pytest.mark.django_db
def test_prestige_character_class_create_view_fail(
    client, prestige_class_fixture, die_fixture, bab_progression_fixture
):
    data = {
        "name": "Grog",
        "max_level": 10,
        "skill_points_per_level": 8,
        "hit_die": die_fixture[2].id,
        "bab_progression": bab_progression_fixture[2].id,
        "required_bab": 5,
    }

    response = client.post(
        "/api/character_class/prestige_character_classes/", data, format="json"
    )

    assert response.status_code == 400
    assert "name" in response.data
    assert "character class with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_prestige_character_class_edit_view(client, prestige_class_fixture):
    prestige_class = prestige_class_fixture[0]
    updated_data = {
        "name": "Updated Grog",
        "max_level": 15,
        "skill_points_per_level": 10,
        "hit_die": prestige_class.hit_die.id,
        "bab_progression": prestige_class.bab_progression.id,
        "required_bab": 8,
    }

    response = client.put(
        f"/api/character_class/prestige_character_classes/{prestige_class.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Grog"
    assert response.data["max_level"] == 15
    assert response.data["required_bab"] == 8


@pytest.mark.django_db
def test_prestige_character_class_delete_view(client, prestige_class_fixture):
    prestige_class = prestige_class_fixture[0]

    response = client.delete(
        f"/api/character_class/prestige_character_classes/{prestige_class.id}/"
    )

    assert response.status_code == 204
    assert not PrestigeCharacterClass.objects.filter(id=prestige_class.id).exists()


@pytest.mark.django_db
def test_prestige_class_skill_rank_requirement_list_view(
    client, prestige_class_skill_rank_requirement_fixture
):
    response = client.get(
        "/api/character_class/prestige_class_skill_rank_requirements/"
    )

    assert response.status_code == 200
    assert len(response.data) == len(prestige_class_skill_rank_requirement_fixture)
    assert {req["prestige_class"] for req in response.data} == {
        req.prestige_class.id for req in prestige_class_skill_rank_requirement_fixture
    }
    assert {req["skill"] for req in response.data} == {
        req.skill.id for req in prestige_class_skill_rank_requirement_fixture
    }


@pytest.mark.django_db
def test_prestige_class_skill_rank_requirement_create_view_success(
    client, prestige_class_fixture, skill_fixture
):
    data = {
        "prestige_class": prestige_class_fixture[0].id,
        "skill": skill_fixture[0].id,
        "required_ranks": 5,
    }

    response = client.post(
        "/api/character_class/prestige_class_skill_rank_requirements/",
        data,
        format="json",
    )

    assert response.status_code == 201
    assert response.data["prestige_class"] == prestige_class_fixture[0].id
    assert response.data["skill"] == skill_fixture[0].id
    assert response.data["required_ranks"] == 5


@pytest.mark.django_db
def test_prestige_class_skill_rank_requirement_create_view_fail(
    client,
    prestige_class_skill_rank_requirement_fixture,
    prestige_class_fixture,
    skill_fixture,
):
    data = {
        "prestige_class": prestige_class_fixture[0].id,
        "skill": skill_fixture[0].id,
        "required_ranks": 5,
    }

    response = client.post(
        "/api/character_class/prestige_class_skill_rank_requirements/",
        data,
        format="json",
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields prestige_class, skill must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_prestige_class_skill_rank_requirement_edit_view(
    client, prestige_class_skill_rank_requirement_fixture
):
    requirement = prestige_class_skill_rank_requirement_fixture[0]
    updated_data = {
        "prestige_class": requirement.prestige_class.id,
        "skill": requirement.skill.id,
        "required_ranks": 6,
    }

    response = client.put(
        f"/api/character_class/prestige_class_skill_rank_requirements/{requirement.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["required_ranks"] == 6


@pytest.mark.django_db
def test_prestige_class_skill_rank_requirement_delete_view(
    client, prestige_class_skill_rank_requirement_fixture
):
    requirement = prestige_class_skill_rank_requirement_fixture[0]

    response = client.delete(
        f"/api/character_class/prestige_class_skill_rank_requirements/{requirement.id}/"
    )

    assert response.status_code == 204
    assert not PrestigeClassSkillRankRequirement.objects.filter(
        id=requirement.id
    ).exists()


@pytest.mark.django_db
def test_prestige_class_language_requirement_list_view(
    client, prestige_class_language_requirement_fixture
):
    response = client.get("/api/character_class/prestige_class_language_requirements/")

    assert response.status_code == 200
    assert len(response.data) == len(prestige_class_language_requirement_fixture)
    assert {pclr["prestige_class"] for pclr in response.data} == {
        pclr.prestige_class.id for pclr in prestige_class_language_requirement_fixture
    }
    assert {pclr["language"] for pclr in response.data} == {
        pclr.language.id for pclr in prestige_class_language_requirement_fixture
    }


@pytest.mark.django_db
def test_prestige_class_language_requirement_create_view_success(
    client, prestige_class_fixture, language_fixture
):
    data = {
        "prestige_class": prestige_class_fixture[0].id,
        "language": language_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/prestige_class_language_requirements/",
        data,
        format="json",
    )

    assert response.status_code == 201
    assert response.data["prestige_class"] == prestige_class_fixture[0].id
    assert response.data["language"] == language_fixture[0].id


@pytest.mark.django_db
def test_prestige_class_language_requirement_create_view_fail(
    client,
    prestige_class_language_requirement_fixture,
    prestige_class_fixture,
    language_fixture,
):
    data = {
        "prestige_class": prestige_class_fixture[0].id,
        "language": language_fixture[0].id,
    }

    response = client.post(
        "/api/character_class/prestige_class_language_requirements/",
        data,
        format="json",
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields prestige_class, language must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_prestige_class_language_requirement_edit_view(
    client, prestige_class_language_requirement_fixture
):
    pclr = prestige_class_language_requirement_fixture[0]
    updated_data = {
        "prestige_class": pclr.prestige_class.id,
        "language": pclr.language.id,
    }

    response = client.put(
        f"/api/character_class/prestige_class_language_requirements/{pclr.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["prestige_class"] == pclr.prestige_class.id
    assert response.data["language"] == pclr.language.id


@pytest.mark.django_db
def test_prestige_class_language_requirement_delete_view(
    client, prestige_class_language_requirement_fixture
):
    pclr = prestige_class_language_requirement_fixture[0]

    response = client.delete(
        f"/api/character_class/prestige_class_language_requirements/{pclr.id}/"
    )

    assert response.status_code == 204
    assert not PrestigeClassLanguageRequirement.objects.filter(id=pclr.id).exists()
