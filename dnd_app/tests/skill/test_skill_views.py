import pytest

from skill.models import Skill


@pytest.mark.django_db
def test_skill_list_view(client, skill_fixture):
    response = client.get("/api/skill/skill/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {skill["name"] for skill in response.data} == {
        skill.name for skill in skill_fixture
    }


@pytest.mark.django_db
def test_skill_create_view_success(client, ability_fixture):
    data = {
        "name": "Running",
        "trained_only": False,
        "armor_check_penalty": False,
        "description": "Fast feet",
        "link": "https://xdd.com",
        "ability": ability_fixture[0].id,
    }

    response = client.post("/api/skill/skill/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Running"
    assert response.data["description"] == "Fast feet"
    assert response.data["link"] == "https://xdd.com"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_errors",
    [
        (
            {
                "name": "Coding",
                "trained_only": False,
                "armor_check_penalty": False,
                "description": "Doing da thing",
                "link": "invalid",
            },
            {
                "name": ["skill with this name already exists."],
                "link": ["Enter a valid URL."],
            },
        ),
    ],
)
def test_skill_create_view_fail(client, data, expected_errors, skill_fixture):
    response = client.post("/api/skill/skill/", data, format="json")

    assert response.status_code == 400

    for field, error_messages in expected_errors.items():
        assert field in response.data
        for error_message in error_messages:
            assert error_message in response.data[field]


@pytest.mark.django_db
def test_skill_edit_view(client, skill_fixture, ability_fixture):
    skill = skill_fixture[0]
    updated_data = {
        "name": "Advanced Coding",
        "trained_only": False,
        "armor_check_penalty": False,
        "description": "Now doing the thing at expert level",
        "ability": ability_fixture[0].id,
    }

    response = client.put(f"/api/skill/skill/{skill.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Advanced Coding"
    assert response.data["description"] == "Now doing the thing at expert level"


@pytest.mark.django_db
def test_skill_delete_view(client, skill_fixture):
    skill = skill_fixture[0]

    response = client.delete(f"/api/skill/skill/{skill.id}/")

    assert response.status_code == 204
    assert not Skill.objects.filter(id=skill.id).exists()
