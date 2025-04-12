import pytest

from feat.models import (
    TypeOfFeat,
    Feat,
    FeatTypeOfFeat,
    FeatAbilityPrerequisite,
    FeatFeatPrerequisite,
    FeatSkillPrerequisite,
)


@pytest.mark.django_db
def test_type_of_feat_list_view(client, type_of_feat_fixture):
    response = client.get("/api/feat/types_of_feats/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {feat["name"] for feat in response.data} == {
        feat.name for feat in type_of_feat_fixture
    }


@pytest.mark.django_db
def test_type_of_feat_create_view_success(client):
    data = {"name": "Specialized", "description": "Highly specialized feats"}

    response = client.post("/api/feat/types_of_feats/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Specialized"
    assert response.data["description"] == "Highly specialized feats"


@pytest.mark.django_db
def test_type_of_feat_create_view_fail(client, type_of_feat_fixture):
    data = {"name": "General", "description": "Well it's general"}

    response = client.post("/api/feat/types_of_feats/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "type of feat with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_type_of_feat_edit_view(client, type_of_feat_fixture):
    feat = type_of_feat_fixture[0]
    updated_data = {
        "name": "Updated General",
        "description": "A more general general feat",
    }

    response = client.put(
        f"/api/feat/types_of_feats/{feat.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated General"
    assert response.data["description"] == "A more general general feat"


@pytest.mark.django_db
def test_type_of_feat_delete_view(client, type_of_feat_fixture):
    feat = type_of_feat_fixture[0]

    response = client.delete(f"/api/feat/types_of_feats/{feat.id}/")

    assert response.status_code == 204
    assert not TypeOfFeat.objects.filter(id=feat.id).exists()


@pytest.mark.django_db
def test_feat_list_view(client, feat_fixture):
    response = client.get("/api/feat/feats/")

    assert response.status_code == 200
    assert len(response.data) == 4
    assert {feat["name"] for feat in response.data} == {
        feat.name for feat in feat_fixture
    }


@pytest.mark.django_db
def test_feat_create_view_success(client, type_of_feat_fixture):
    data = {
        "name": "Feat 5",
        "benefit": "Benefit 5",
        "feat_type": [type_of_feat_fixture[0].id],
    }

    response = client.post("/api/feat/feats/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Feat 5"
    assert response.data["benefit"] == "Benefit 5"
    assert response.data["feat_type"] == [type_of_feat_fixture[0].id]

    # Check if M2M relationship is created
    assert FeatTypeOfFeat.objects.filter(
        feat=response.data["id"], type_of_feat=type_of_feat_fixture[0]
    ).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_errors",
    [
        (
            {
                "name": "Feat 1",
                "benefit": "Benefit 1",
                "feat_type": [],
                "link": "invalid_url",
            },
            {
                "name": ["feat with this name already exists."],
                "link": ["Enter a valid URL."],
            },
        ),
        (
            {},
            {
                "name": ["This field is required."],
                "benefit": ["This field is required."],
                "feat_type": ["This field is required."],
            },
        ),
    ],
)
def test_feat_create_view_fail(
    client, data, expected_errors, feat_fixture, type_of_feat_fixture
):
    if "feat_type" in data:
        data["feat_type"] = [type_of_feat_fixture[0].id]

    response = client.post("/api/feat/feats/", data, format="json")

    assert response.status_code == 400

    for field, error_messages in expected_errors.items():
        assert field in response.data
        for error_message in error_messages:
            assert error_message in response.data[field]


@pytest.mark.django_db
def test_feat_edit_view(client, feat_fixture, type_of_feat_fixture):
    feat = feat_fixture[0]
    updated_data = {
        "name": "Updated Feat 1",
        "benefit": "Updated Benefit 1",
        "feat_type": [type_of_feat_fixture[0].id],
    }

    response = client.put(f"/api/feat/feats/{feat.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Feat 1"
    assert response.data["benefit"] == "Updated Benefit 1"
    assert response.data["feat_type"] == [type_of_feat_fixture[0].id]


@pytest.mark.django_db
def test_feat_delete_view_success(
    client,
    feat_fixture,
    feat_type_of_feat_fixture,
    feat_ability_prerequisite_fixture,
    feat_feat_prerequisite_fixture,
    feat_skill_prerequisite_fixture,
):
    feat = feat_fixture[0]  # Feat that's not a prerequisite for any other feat

    # Ensure the feat has all M2M relationships
    assert FeatTypeOfFeat.objects.filter(feat=feat).exists()
    assert FeatAbilityPrerequisite.objects.filter(feat=feat).exists()
    # this feat has other feats as prerequisites
    # but there are no feats that have this feat as prerequisite
    assert FeatFeatPrerequisite.objects.filter(prerequisite_for_feat=feat).exists()
    assert not FeatFeatPrerequisite.objects.filter(prerequisite=feat).exists()
    assert FeatSkillPrerequisite.objects.filter(feat=feat).exists()

    response = client.delete(f"/api/feat/feats/{feat.id}/")

    assert response.status_code == 204
    assert not Feat.objects.filter(id=feat.id).exists()
    assert not FeatTypeOfFeat.objects.filter(feat=feat).exists()
    assert not FeatAbilityPrerequisite.objects.filter(feat=feat).exists()
    assert not FeatFeatPrerequisite.objects.filter(prerequisite_for_feat=feat).exists()


@pytest.mark.django_db
def test_feat_delete_view_fail(
    client,
    feat_fixture,
    feat_type_of_feat_fixture,
    feat_ability_prerequisite_fixture,
    feat_feat_prerequisite_fixture,
    feat_skill_prerequisite_fixture,
):
    feat = feat_fixture[1]

    # Ensure the feat has all M2M relationships
    assert FeatTypeOfFeat.objects.filter(feat=feat).exists()
    assert FeatAbilityPrerequisite.objects.filter(feat=feat).exists()
    # this feat has no other feats as prerequisites
    # but there are feats that have this feat as prerequisite
    assert not FeatFeatPrerequisite.objects.filter(prerequisite_for_feat=feat).exists()
    assert FeatFeatPrerequisite.objects.filter(prerequisite=feat).exists()
    assert FeatSkillPrerequisite.objects.filter(feat=feat).exists()

    response = client.delete(f"/api/feat/feats/{feat.id}/")

    assert response.status_code == 400
    assert "detail" in response.data
    assert (
        "This object cannot be deleted because it has dependent objects."
        in response.data["detail"]
    )

    # Nothing should be deleted
    assert Feat.objects.filter(id=feat.id).exists()
    assert FeatTypeOfFeat.objects.filter(feat=feat).exists()
    assert FeatAbilityPrerequisite.objects.filter(feat=feat).exists()
    assert not FeatFeatPrerequisite.objects.filter(prerequisite_for_feat=feat).exists()
    assert FeatFeatPrerequisite.objects.filter(prerequisite=feat).exists()
    assert FeatSkillPrerequisite.objects.filter(feat=feat).exists()
