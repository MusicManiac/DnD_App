from datetime import datetime

import pytest
from django.urls import reverse

from common.models import (
    Source,
    Die,
    TraitClassification,
    Trait,
    Ability,
    Alignment,
    Language,
)


@pytest.mark.django_db
def test_source_list_view(client, source_fixture):
    response = client.get("/api/common/sources/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {source["name"] for source in response.data} == {
        source.name for source in source_fixture
    }


@pytest.mark.django_db
def test_source_create_view_success(client):
    data = {"name": "Player's Handbook", "year": 2022}

    response = client.post("/api/common/sources/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Player's Handbook"
    assert response.data["year"] == 2022


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_errors",
    [
        (
            {"name": "PHB", "year": 1111, "link": "invalid_url"},
            {
                "name": ["source with this name already exists."],
                "year": [f"Year must be between 1974 and {datetime.now().year}."],
                "link": ["Enter a valid URL."],
            },
        ),
    ],
)
def test_source_create_view_fail(client, data, expected_errors, source_fixture):
    response = client.post(reverse("source-list"), data, format="json")

    assert response.status_code == 400

    for field, error_messages in expected_errors.items():
        assert field in response.data
        for error_message in error_messages:
            assert error_message in response.data[field]


@pytest.mark.django_db
def test_source_delete_view(client, source_fixture):
    response = client.delete(f"/api/common/sources/{source_fixture[0].id}/")

    assert response.status_code == 204
    assert not Source.objects.filter(id=source_fixture[0].id).exists()


@pytest.mark.django_db
def test_source_edit_view(client, source_fixture):
    updated_data = {"name": "Updated PHB", "year": 2021}

    response = client.put(
        f"/api/common/sources/{source_fixture[0].id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated PHB"
    assert response.data["year"] == 2021


@pytest.mark.django_db
def test_die_list_view(client, die_fixture):
    response = client.get("/api/common/dice/")

    assert response.status_code == 200
    assert len(response.data) == 3
    assert {die["sides"] for die in response.data} == {
        dice.sides for dice in die_fixture
    }


@pytest.mark.django_db
def test_die_create_view_success(client):
    data = {"sides": 8}

    response = client.post("/api/common/dice/", data, format="json")

    assert response.status_code == 201
    assert response.data["sides"] == 8


@pytest.mark.django_db
def test_die_create_view_fail(client, die_fixture):
    data = {"sides": 2}

    response = client.post("/api/common/dice/", data, format="json")

    assert response.status_code == 400
    assert "sides" in response.data
    assert "die with this sides already exists." in response.data["sides"]


@pytest.mark.django_db
def test_die_delete_view(client, die_fixture):
    die = die_fixture[0]

    response = client.delete(f"/api/common/dice/{die.id}/")

    assert response.status_code == 204
    assert not Die.objects.filter(id=die.id).exists()


@pytest.mark.django_db
def test_die_edit_view(client, die_fixture):
    die = die_fixture[0]
    updated_data = {"sides": 12}

    response = client.put(f"/api/common/dice/{die.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["sides"] == 12


@pytest.mark.django_db
def test_trait_classification_list_view(client, trait_classification_fixture):
    response = client.get("/api/common/trait_classifications/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {tc["name"] for tc in response.data} == {
        tc.name for tc in trait_classification_fixture
    }


@pytest.mark.django_db
def test_trait_classification_create_view_success(client):
    data = {"name": "Damage", "description": "Big bonk"}

    response = client.post("/api/common/trait_classifications/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Damage"


@pytest.mark.django_db
def test_trait_classification_create_view_fail(client, trait_classification_fixture):
    data = {"name": "Attack"}

    response = client.post("/api/common/trait_classifications/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert (
        "trait classification with this name already exists." in response.data["name"]
    )


@pytest.mark.django_db
def test_trait_classification_edit_view(client, trait_classification_fixture):
    trait_classification = trait_classification_fixture[0]
    updated_data = {"name": "Edited", "description": "brrrrrr"}

    response = client.put(
        f"/api/common/trait_classifications/{trait_classification.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Edited"


@pytest.mark.django_db
def test_trait_classification_delete_view(client, trait_classification_fixture):
    trait_classification = trait_classification_fixture[0]

    response = client.delete(
        f"/api/common/trait_classifications/{trait_classification.id}/"
    )

    assert response.status_code == 204
    assert not TraitClassification.objects.filter(id=trait_classification.id).exists()


@pytest.mark.django_db
def test_trait_list_view(client, trait_fixture):
    response = client.get("/api/common/traits/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {trait["short_description"] for trait in response.data} == {
        trait.short_description for trait in trait_fixture
    }


@pytest.mark.django_db
def test_trait_create_view_success(client, trait_classification_fixture):
    data = {
        "short_description": "Fire Resistance",
        "long_description": "They see me burnin' they hatin'",
        "trait_classification": trait_classification_fixture[0].id,
    }

    response = client.post("/api/common/traits/", data, format="json")

    assert response.status_code == 201
    assert response.data["short_description"] == "Fire Resistance"
    assert response.data["long_description"] == "They see me burnin' they hatin'"


@pytest.mark.django_db
def test_trait_create_view_fail(client, trait_fixture, trait_classification_fixture):
    data = {
        "short_description": "Darkvision",
        "long_description": "Ability to see in the dark.",
        "trait_classification": trait_classification_fixture[0].id,
    }

    response = client.post("/api/common/traits/", data, format="json")

    assert response.status_code == 400
    assert "short_description" in response.data
    assert (
        "trait with this short description already exists."
        in response.data["short_description"]
    )


@pytest.mark.django_db
def test_trait_edit_view(client, trait_fixture, trait_classification_fixture):
    trait = trait_fixture[0]
    updated_data = {
        "short_description": "Improved Darkvision",
        "long_description": "Ability to see in the dark with greater clarity.",
        "trait_classification": trait_classification_fixture[0].id,
    }

    response = client.put(
        f"/api/common/traits/{trait.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["short_description"] == "Improved Darkvision"
    assert (
        response.data["long_description"]
        == "Ability to see in the dark with greater clarity."
    )


@pytest.mark.django_db
def test_trait_delete_view(client, trait_fixture):
    trait = trait_fixture[0]

    response = client.delete(f"/api/common/traits/{trait.id}/")

    assert response.status_code == 204
    assert not Trait.objects.filter(id=trait.id).exists()


@pytest.mark.django_db
def test_duration_unit_list_view(client, duration_unit_fixture):
    response = client.get("/api/common/duration_units/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {duration_unit["name"] for duration_unit in response.data} == {
        du.name for du in duration_unit_fixture
    }


@pytest.mark.django_db
def test_duration_unit_create_view_success(client):
    data = {"name": "Minute", "name_plural": "Minutes", "duration_in_seconds": 60}

    response = client.post("/api/common/duration_units/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Minute"
    assert response.data["name_plural"] == "Minutes"
    assert response.data["duration_in_seconds"] == 60


@pytest.mark.django_db
def test_duration_unit_create_view_fail(client, duration_unit_fixture):
    data = {"name": "Second", "name_plural": "Seconds", "duration_in_seconds": 1}

    response = client.post("/api/common/duration_units/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "duration unit with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_duration_unit_edit_view(client, duration_unit_fixture):
    duration_unit = duration_unit_fixture[0]
    updated_data = {
        "name": "Updated Second",
        "name_plural": "Updated Seconds",
        "duration_in_seconds": 2,
    }

    response = client.put(
        f"/api/common/duration_units/{duration_unit.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Second"
    assert response.data["name_plural"] == "Updated Seconds"
    assert response.data["duration_in_seconds"] == 2


@pytest.mark.django_db
def test_duration_unit_delete_view(client, duration_unit_fixture):
    duration_unit = duration_unit_fixture[0]

    response = client.delete(f"/api/common/duration_units/{duration_unit.id}/")

    assert response.status_code == 204


@pytest.mark.django_db
def test_ability_list_view(client, ability_fixture):
    response = client.get("/api/common/abilities/")

    assert response.status_code == 200
    assert len(response.data) == 3
    assert {ability["name"] for ability in response.data} == {
        ability.name for ability in ability_fixture
    }


@pytest.mark.django_db
def test_ability_create_view_success(client):
    data = {
        "name": "Constitution",
        "abbreviation": "CON",
        "description": "Me tough, me last!",
    }

    response = client.post("/api/common/abilities/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Constitution"
    assert response.data["abbreviation"] == "CON"
    assert response.data["description"] == "Me tough, me last!"


@pytest.mark.django_db
def test_ability_create_view_fail(client, ability_fixture):
    data = {
        "name": "Strength",
        "abbreviation": "STR",
        "description": "Me strong, me smash!",
    }

    response = client.post("/api/common/abilities/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "ability with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_ability_edit_view(client, ability_fixture):
    ability = ability_fixture[0]
    updated_data = {
        "name": "Improved Strength",
        "abbreviation": "STR",
        "description": "Now even stronger!",
    }

    response = client.put(
        f"/api/common/abilities/{ability.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Improved Strength"
    assert response.data["description"] == "Now even stronger!"


@pytest.mark.django_db
def test_ability_delete_view(client, ability_fixture):
    ability = ability_fixture[0]

    response = client.delete(f"/api/common/abilities/{ability.id}/")

    assert response.status_code == 204
    assert not Ability.objects.filter(id=ability.id).exists()


@pytest.mark.django_db
def test_alignment_list_view(client, alignment_fixture):
    response = client.get("/api/common/alignments/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {alignment["name"] for alignment in response.data} == {
        alignment.name for alignment in alignment_fixture
    }


@pytest.mark.django_db
def test_alignment_create_view_success(client):
    data = {
        "name": "Neutral Good",
        "abbreviation": "NG",
        "description": "The good guys who aren't tied down by laws.",
    }

    response = client.post("/api/common/alignments/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Neutral Good"
    assert response.data["abbreviation"] == "NG"
    assert response.data["description"] == "The good guys who aren't tied down by laws."


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_errors",
    [
        (
            {
                "name": "Lawful Good",
                "abbreviation": "LG",
                "description": "Paladin and stuff",
            },
            {
                "name": ["alignment with this name already exists."],
                "abbreviation": ["alignment with this abbreviation already exists."],
            },
        ),
    ],
)
def test_alignment_create_view_fail(client, data, expected_errors, alignment_fixture):
    response = client.post("/api/common/alignments/", data, format="json")

    assert response.status_code == 400

    for field, error_messages in expected_errors.items():
        assert field in response.data
        for error_message in error_messages:
            assert error_message in response.data[field]


@pytest.mark.django_db
def test_alignment_edit_view(client, alignment_fixture):
    alignment = alignment_fixture[0]
    updated_data = {
        "name": "Lawful Neutral",
        "abbreviation": "LN",
        "description": "The law is the law, no matter what.",
    }

    response = client.put(
        f"/api/common/alignments/{alignment.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Lawful Neutral"
    assert response.data["description"] == "The law is the law, no matter what."


@pytest.mark.django_db
def test_alignment_delete_view(client, alignment_fixture):
    alignment = alignment_fixture[0]

    response = client.delete(f"/api/common/alignments/{alignment.id}/")

    assert response.status_code == 204
    assert not Alignment.objects.filter(id=alignment.id).exists()


@pytest.mark.django_db
def test_language_list_view(client, language_fixture):
    response = client.get("/api/common/languages/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {language["name"] for language in response.data} == {
        language.name for language in language_fixture
    }


@pytest.mark.django_db
def test_language_create_view_success(client, source_fixture):
    data = {"name": "Dwarvish", "alphabet": "Dwarven", "source": source_fixture[0].id}

    response = client.post("/api/common/languages/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Dwarvish"
    assert response.data["alphabet"] == "Dwarven"
    assert response.data["source"] == source_fixture[0].id


@pytest.mark.django_db
def test_language_create_view_fail(client, language_fixture, source_fixture):
    data = {"name": "Common", "alphabet": "Common", "source": source_fixture[0].id}

    response = client.post("/api/common/languages/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "language with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_language_edit_view(client, language_fixture, source_fixture):
    language = language_fixture[0]
    updated_data = {
        "name": "Updated Common",
        "alphabet": "Updated Common Alphabet",
        "source": source_fixture[0].id,
    }

    response = client.put(
        f"/api/common/languages/{language.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Common"
    assert response.data["alphabet"] == "Updated Common Alphabet"


@pytest.mark.django_db
def test_language_delete_view(client, language_fixture):
    language = language_fixture[0]

    response = client.delete(f"/api/common/languages/{language.id}/")

    assert response.status_code == 204
    assert not Language.objects.filter(id=language.id).exists()
