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


@pytest.mark.django_db
def test_ability_modifier_list_view(client, ability_modifier_fixture):
    response = client.get("/api/race/ability_modifier/")

    assert response.status_code == 200
    assert len(response.data) == len(ability_modifier_fixture)
    assert {modifier["value"] for modifier in response.data} == {
        modifier.value for modifier in ability_modifier_fixture
    }


@pytest.mark.django_db
def test_ability_modifier_create_view_success(client, ability_fixture):
    data = {"value": 5, "ability": ability_fixture[0].id}

    response = client.post("/api/race/ability_modifier/", data, format="json")

    assert response.status_code == 201
    assert response.data["value"] == 5
    assert response.data["ability"] == ability_fixture[0].id


@pytest.mark.django_db
def test_ability_modifier_create_view_fail(
    client, ability_modifier_fixture, ability_fixture
):
    data = {"value": 2, "ability": ability_fixture[0].id}
    response = client.post("/api/race/ability_modifier/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields value, ability must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_ability_modifier_edit_view(client, ability_modifier_fixture):
    ability_modifier = ability_modifier_fixture[0]
    updated_data = {"value": 4, "ability": ability_modifier.ability.id}

    response = client.put(
        f"/api/race/ability_modifier/{ability_modifier.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["value"] == 4
    assert response.data["ability"] == ability_modifier.ability.id


@pytest.mark.django_db
def test_ability_modifier_delete_view(client, ability_modifier_fixture):
    ability_modifier = ability_modifier_fixture[0]

    response = client.delete(f"/api/race/ability_modifier/{ability_modifier.id}/")

    assert response.status_code == 204
    assert not AbilityModifier.objects.filter(id=ability_modifier.id).exists()


@pytest.mark.django_db
def test_size_list_view(client, size_fixture):
    response = client.get("/api/race/size/")

    assert response.status_code == 200
    assert len(response.data) == len(size_fixture)
    assert {size["name"] for size in response.data} == {
        size.name for size in size_fixture
    }


@pytest.mark.django_db
def test_size_create_view_success(client):
    data = {
        "name": "Huge",
        "size_modifier": -4,
        "grapple_modifier": 4,
        "height_or_length": "16-32 ft",
        "weight": "800-1600 lbs",
        "space_ft": 15.0,
        "natural_reach_tall_ft": 15,
        "natural_reach_long_ft": 15,
    }

    response = client.post("/api/race/size/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Huge"
    assert response.data["size_modifier"] == -4
    assert response.data["grapple_modifier"] == 4
    assert response.data["height_or_length"] == "16-32 ft"
    assert response.data["weight"] == "800-1600 lbs"
    assert response.data["space_ft"] == "15.0"
    assert response.data["natural_reach_tall_ft"] == 15
    assert response.data["natural_reach_long_ft"] == 15


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_errors",
    [
        (
            {
                "name": "Small",
                "size_modifier": 1,
                "grapple_modifier": -1,
                "height_or_length": "2-4 ft",
                "weight": "20-40 lbs",
                "space_ft": 5.0,
                "natural_reach_tall_ft": 0,
                "natural_reach_long_ft": 0,
            },
            {"name": ["size with this name already exists."]},
        ),
        (
            {},
            {
                "name": ["This field is required."],
                "height_or_length": ["This field is required."],
                "weight": ["This field is required."],
                "space_ft": ["This field is required."],
            },
        ),
    ],
)
def test_size_create_view_fail(client, data, expected_errors, size_fixture):
    response = client.post("/api/race/size/", data, format="json")

    assert response.status_code == 400

    for field, error_messages in expected_errors.items():
        assert field in response.data
        for error_message in error_messages:
            assert error_message in response.data[field]


@pytest.mark.django_db
def test_size_edit_view(client, size_fixture):
    size = size_fixture[0]
    updated_data = {
        "name": "Small (Updated)",
        "size_modifier": 2,
        "grapple_modifier": -1,
        "height_or_length": "2.5-4.5 ft",
        "weight": "25-45 lbs",
        "space_ft": 5.0,
        "natural_reach_tall_ft": 0,
        "natural_reach_long_ft": 0,
    }

    response = client.put(f"/api/race/size/{size.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Small (Updated)"
    assert response.data["size_modifier"] == 2
    assert response.data["height_or_length"] == "2.5-4.5 ft"


@pytest.mark.django_db
def test_size_delete_view(client, size_fixture):
    size = size_fixture[0]

    response = client.delete(f"/api/race/size/{size.id}/")

    assert response.status_code == 204
    assert not Size.objects.filter(id=size.id).exists()


@pytest.mark.django_db
def test_character_type_list_view(client, character_type_fixture):
    response = client.get("/api/race/character_type/")

    assert response.status_code == 200
    assert len(response.data) == len(character_type_fixture)
    assert {char_type["name"] for char_type in response.data} == {
        ct.name for ct in character_type_fixture
    }


@pytest.mark.django_db
def test_character_type_create_view_success(client):
    data = {"name": "Beast"}

    response = client.post("/api/race/character_type/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Beast"


@pytest.mark.django_db
def test_character_type_create_view_fail(client, character_type_fixture):
    data = {
        "name": "Humanoid",
    }

    response = client.post("/api/race/character_type/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "character type with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_character_type_edit_view(client, character_type_fixture):
    char_type = character_type_fixture[0]
    updated_data = {"name": "Updated Humanoid"}

    response = client.put(
        f"/api/race/character_type/{char_type.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Humanoid"


@pytest.mark.django_db
def test_character_type_delete_view(client, character_type_fixture):
    char_type = character_type_fixture[0]

    response = client.delete(f"/api/race/character_type/{char_type.id}/")

    assert response.status_code == 204
    assert not CharacterType.objects.filter(id=char_type.id).exists()


@pytest.mark.django_db
def test_character_type_trait_list_view(client, character_type_trait_fixture):
    response = client.get("/api/race/character_type_trait/")

    assert response.status_code == 200
    assert len(response.data) == len(character_type_trait_fixture)
    assert {ctt["character_type"] for ctt in response.data} == {
        ctt.character_type.id for ctt in character_type_trait_fixture
    }
    assert {ctt["trait"] for ctt in response.data} == {
        ctt.trait.id for ctt in character_type_trait_fixture
    }


@pytest.mark.django_db
def test_character_type_trait_create_view_success(
    client, character_type_fixture, trait_fixture
):
    data = {
        "character_type": character_type_fixture[0].id,
        "trait": trait_fixture[0].id,
    }

    response = client.post("/api/race/character_type_trait/", data, format="json")

    assert response.status_code == 201
    assert response.data["character_type"] == character_type_fixture[0].id
    assert response.data["trait"] == trait_fixture[0].id


@pytest.mark.django_db
def test_character_type_trait_create_view_fail(
    client, character_type_trait_fixture, character_type_fixture, trait_fixture
):
    data = {
        "character_type": character_type_fixture[0].id,
        "trait": trait_fixture[0].id,
    }

    response = client.post("/api/race/character_type_trait/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields character_type, trait must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_character_type_trait_edit_view(client, character_type_trait_fixture):
    ctt = character_type_trait_fixture[0]
    updated_data = {"character_type": ctt.character_type.id, "trait": ctt.trait.id}

    response = client.put(
        f"/api/race/character_type_trait/{ctt.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["character_type"] == ctt.character_type.id
    assert response.data["trait"] == ctt.trait.id


@pytest.mark.django_db
def test_character_type_trait_delete_view(client, character_type_trait_fixture):
    ctt = character_type_trait_fixture[0]

    response = client.delete(f"/api/race/character_type_trait/{ctt.id}/")

    assert response.status_code == 204
    assert not CharacterTypeTrait.objects.filter(id=ctt.id).exists()


@pytest.mark.django_db
def test_race_list_view(client, race_fixture):
    response = client.get("/api/race/race/")

    assert response.status_code == 200
    assert len(response.data) == len(race_fixture)
    assert {race["name"] for race in response.data} == {
        race.name for race in race_fixture
    }


@pytest.mark.django_db
def test_race_create_view_success(client, size_fixture, source_fixture):
    data = {
        "name": "Elf",
        "description": "Elffff.",
        "link": "https://www.elf.com",
        "level_adjustment": 0,
        "size": size_fixture[1].id,
        "source": source_fixture[0].id,
    }

    response = client.post("/api/race/race/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Elf"
    assert response.data["description"] == "Elffff."
    assert response.data["size"] == size_fixture[1].id
    assert response.data["source"] == source_fixture[0].id


@pytest.mark.django_db
def test_race_create_view_fail(client, race_fixture, size_fixture, source_fixture):
    data = {
        "name": "Human",
        "description": "Sum desc",
        "link": "https://www.human.com",
        "level_adjustment": 0,
        "size": size_fixture[1].id,
        "source": source_fixture[0].id,
    }

    response = client.post("/api/race/race/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "race with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_race_edit_view(client, race_fixture, size_fixture, source_fixture):
    race = race_fixture[0]
    updated_data = {
        "name": "Updated Human",
        "description": "Updated description",
        "link": "https://www.updatedhuman.com",
        "level_adjustment": 1,
        "size": size_fixture[2].id,
        "source": source_fixture[1].id,
    }

    response = client.put(f"/api/race/race/{race.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Human"
    assert response.data["description"] == "Updated description"
    assert response.data["size"] == size_fixture[2].id
    assert response.data["source"] == source_fixture[1].id


@pytest.mark.django_db
def test_race_delete_view(client, race_fixture):
    race = race_fixture[0]

    response = client.delete(f"/api/race/race/{race.id}/")

    assert response.status_code == 204
    assert not Race.objects.filter(id=race.id).exists()


@pytest.mark.django_db
def test_race_type_list_view(client, race_type_fixture):
    response = client.get("/api/race/race_type/")

    assert response.status_code == 200
    assert len(response.data) == len(race_type_fixture)
    assert {race_type["race"] for race_type in response.data} == {
        rt.race.id for rt in race_type_fixture
    }
    assert {race_type["character_type"] for race_type in response.data} == {
        rt.character_type.id for rt in race_type_fixture
    }


@pytest.mark.django_db
def test_race_type_create_view_success(client, race_fixture, character_type_fixture):
    data = {"race": race_fixture[0].id, "character_type": character_type_fixture[0].id}

    response = client.post("/api/race/race_type/", data, format="json")

    assert response.status_code == 201
    assert response.data["race"] == race_fixture[0].id
    assert response.data["character_type"] == character_type_fixture[0].id


@pytest.mark.django_db
def test_race_type_create_view_fail(
    client, race_type_fixture, race_fixture, character_type_fixture
):
    data = {
        "race": race_fixture[0].id,
        "character_type": character_type_fixture[0].id,
    }

    response = client.post("/api/race/race_type/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields race, character_type must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_race_type_edit_view(client, race_type_fixture):
    race_type = race_type_fixture[0]
    updated_data = {
        "race": race_type.race.id,
        "character_type": race_type.character_type.id,
    }

    response = client.put(
        f"/api/race/race_type/{race_type.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["race"] == race_type.race.id
    assert response.data["character_type"] == race_type.character_type.id


@pytest.mark.django_db
def test_race_type_delete_view(client, race_type_fixture):
    race_type = race_type_fixture[0]

    response = client.delete(f"/api/race/race_type/{race_type.id}/")

    assert response.status_code == 204
    assert not RaceType.objects.filter(id=race_type.id).exists()


@pytest.mark.django_db
def test_race_ability_modifier_list_view(client, race_ability_modifier_fixture):
    response = client.get("/api/race/race_ability_modifier/")

    assert response.status_code == 200
    assert len(response.data) == len(race_ability_modifier_fixture)
    assert {modifier["race"] for modifier in response.data} == {
        ram.race.id for ram in race_ability_modifier_fixture
    }
    assert {modifier["ability_modifier"] for modifier in response.data} == {
        ram.ability_modifier.id for ram in race_ability_modifier_fixture
    }


@pytest.mark.django_db
def test_race_ability_modifier_create_view_success(
    client, race_fixture, ability_modifier_fixture
):
    data = {
        "race": race_fixture[0].id,
        "ability_modifier": ability_modifier_fixture[0].id,
    }

    response = client.post("/api/race/race_ability_modifier/", data, format="json")

    assert response.status_code == 201
    assert response.data["race"] == race_fixture[0].id
    assert response.data["ability_modifier"] == ability_modifier_fixture[0].id


@pytest.mark.django_db
def test_race_ability_modifier_create_view_fail(
    client, race_ability_modifier_fixture, race_fixture, ability_modifier_fixture
):
    data = {
        "race": race_fixture[0].id,
        "ability_modifier": ability_modifier_fixture[0].id,
    }

    response = client.post("/api/race/race_ability_modifier/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields race, ability_modifier must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_race_ability_modifier_edit_view(client, race_ability_modifier_fixture):
    race_ability_modifier = race_ability_modifier_fixture[0]
    updated_data = {
        "race": race_ability_modifier.race.id,
        "ability_modifier": race_ability_modifier.ability_modifier.id,
    }

    response = client.put(
        f"/api/race/race_ability_modifier/{race_ability_modifier.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["race"] == race_ability_modifier.race.id
    assert (
        response.data["ability_modifier"] == race_ability_modifier.ability_modifier.id
    )


@pytest.mark.django_db
def test_race_ability_modifier_delete_view(client, race_ability_modifier_fixture):
    race_ability_modifier = race_ability_modifier_fixture[0]

    response = client.delete(
        f"/api/race/race_ability_modifier/{race_ability_modifier.id}/"
    )

    assert response.status_code == 204
    assert not RaceAbilityModifier.objects.filter(id=race_ability_modifier.id).exists()


@pytest.mark.django_db
def test_race_trait_list_view(client, race_trait_fixture):
    response = client.get("/api/race/race_trait/")

    assert response.status_code == 200
    assert len(response.data) == len(race_trait_fixture)
    assert {rt["race"] for rt in response.data} == {
        rt.race.id for rt in race_trait_fixture
    }
    assert {rt["trait"] for rt in response.data} == {
        rt.trait.id for rt in race_trait_fixture
    }


@pytest.mark.django_db
def test_race_trait_create_view_success(client, race_fixture, trait_fixture):
    data = {
        "race": race_fixture[0].id,
        "trait": trait_fixture[0].id,
        "additional_value": "Some additional value",
    }

    response = client.post("/api/race/race_trait/", data, format="json")

    assert response.status_code == 201
    assert response.data["race"] == race_fixture[0].id
    assert response.data["trait"] == trait_fixture[0].id
    assert response.data["additional_value"] == "Some additional value"


@pytest.mark.django_db
def test_race_trait_create_view_fail(
    client, race_trait_fixture, race_fixture, trait_fixture
):
    pass


@pytest.mark.django_db
def test_race_trait_edit_view(client, race_trait_fixture):
    race_trait = race_trait_fixture[0]
    updated_data = {
        "race": race_trait.race.id,
        "trait": race_trait.trait.id,
        "additional_value": "Updated additional value",
    }

    response = client.put(
        f"/api/race/race_trait/{race_trait.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["additional_value"] == "Updated additional value"


@pytest.mark.django_db
def test_race_trait_delete_view(client, race_trait_fixture):
    race_trait = race_trait_fixture[0]

    response = client.delete(f"/api/race/race_trait/{race_trait.id}/")

    assert response.status_code == 204
    assert not RaceTrait.objects.filter(id=race_trait.id).exists()


@pytest.mark.django_db
def test_race_language_list_view(client, race_language_fixture):
    response = client.get("/api/race/race_language/")

    assert response.status_code == 200
    assert len(response.data) == len(race_language_fixture)
    assert {rl["race"] for rl in response.data} == {
        rl.race.id for rl in race_language_fixture
    }
    assert {rl["language"] for rl in response.data} == {
        rl.language.id for rl in race_language_fixture
    }


@pytest.mark.django_db
def test_race_language_create_view_success(client, race_fixture, language_fixture):
    data = {
        "race": race_fixture[0].id,
        "language": language_fixture[0].id,
        "is_automatic": True,
    }

    response = client.post("/api/race/race_language/", data, format="json")

    assert response.status_code == 201
    assert response.data["race"] == race_fixture[0].id
    assert response.data["language"] == language_fixture[0].id
    assert response.data["is_automatic"] is True


@pytest.mark.django_db
def test_race_language_create_view_fail(
    client, race_language_fixture, race_fixture, language_fixture
):
    data = {"race": race_fixture[0].id, "language": language_fixture[0].id}

    response = client.post("/api/race/race_language/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields race, language must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_race_language_edit_view(client, race_language_fixture):
    race_language = race_language_fixture[0]
    updated_data = {
        "race": race_language.race.id,
        "language": race_language.language.id,
        "is_automatic": False,
    }

    response = client.put(
        f"/api/race/race_language/{race_language.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["is_automatic"] is False


@pytest.mark.django_db
def test_race_language_delete_view(client, race_language_fixture):
    race_language = race_language_fixture[0]

    response = client.delete(f"/api/race/race_language/{race_language.id}/")

    assert response.status_code == 204
    assert not RaceLanguage.objects.filter(id=race_language.id).exists()


@pytest.mark.django_db
def test_race_favored_class_list_view(client, race_favored_class_fixture):
    response = client.get("/api/race/race_favored_class/")

    assert response.status_code == 200
    assert len(response.data) == len(race_favored_class_fixture)
    assert {rfc["race"] for rfc in response.data} == {
        rfc.race.id for rfc in race_favored_class_fixture
    }
    assert {rfc["character_class"] for rfc in response.data} == {
        rfc.character_class.id for rfc in race_favored_class_fixture
    }


@pytest.mark.django_db
def test_race_favored_class_create_view_success(
    client, race_fixture, character_class_fixture
):
    data = {
        "race": race_fixture[0].id,
        "character_class": character_class_fixture[0].id,
    }

    response = client.post("/api/race/race_favored_class/", data, format="json")

    assert response.status_code == 201
    assert response.data["race"] == race_fixture[0].id
    assert response.data["character_class"] == character_class_fixture[0].id


@pytest.mark.django_db
def test_race_favored_class_create_view_fail(
    client, race_favored_class_fixture, race_fixture, character_class_fixture
):
    data = {
        "race": race_fixture[0].id,
        "character_class": character_class_fixture[0].id,
    }

    response = client.post("/api/race/race_favored_class/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields race, character_class must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_race_favored_class_edit_view(client, race_favored_class_fixture):
    race_favored_class = race_favored_class_fixture[0]
    updated_data = {
        "race": race_favored_class.race.id,
        "character_class": race_favored_class.character_class.id,
    }

    response = client.put(
        f"/api/race/race_favored_class/{race_favored_class.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["race"] == race_favored_class.race.id
    assert response.data["character_class"] == race_favored_class.character_class.id


@pytest.mark.django_db
def test_race_favored_class_delete_view(client, race_favored_class_fixture):
    race_favored_class = race_favored_class_fixture[0]

    response = client.delete(f"/api/race/race_favored_class/{race_favored_class.id}/")

    assert response.status_code == 204
    assert not RaceFavoredClass.objects.filter(id=race_favored_class.id).exists()
