import pytest


@pytest.mark.django_db
def test_type_of_feat_creation(type_of_feat_fixture):
    type_of_feat = type_of_feat_fixture[0]
    assert type_of_feat.name == "General"
    assert type_of_feat.description == "Well it's general"
    assert str(type_of_feat) == "General"


@pytest.mark.django_db
def test_feat_creation(feat_fixture):
    feat = feat_fixture[0]
    assert feat.name == "Feat 1"
    assert feat.benefit == "Benefit 1"
    assert feat.normal == "Normal 1"
    assert feat.special == "Special 1"
    assert feat.other_prerequisites == "Other prerequisites 1"
    assert feat.link == "https://netflix.com"
    assert str(feat) == "Feat 1"


@pytest.mark.django_db
def test_feat_type_of_feat_creation(feat_type_of_feat_fixture):
    feat_type_of_feat = feat_type_of_feat_fixture[0]
    assert feat_type_of_feat.feat.name == "Feat 1"
    assert feat_type_of_feat.type_of_feat.name == "General"


@pytest.mark.django_db
def test_feat_ability_prerequisite_creation(feat_ability_prerequisite_fixture):
    feat_ability_prerequisite = feat_ability_prerequisite_fixture[0]
    assert feat_ability_prerequisite.feat.name == "Feat 1"
    assert feat_ability_prerequisite.ability.name == "Strength"


@pytest.mark.django_db
def test_feat_feat_prerequisite_creation(feat_feat_prerequisite_fixture):
    feat_feat_prerequisite = feat_feat_prerequisite_fixture[0]
    assert feat_feat_prerequisite.prerequisite_for_feat.name == "Feat 1"
    assert feat_feat_prerequisite.prerequisite.name == "Feat 2"


@pytest.mark.django_db
def test_feat_skill_prerequisite_creation(feat_skill_prerequisite_fixture):
    feat_skill_prerequisite = feat_skill_prerequisite_fixture[0]
    assert feat_skill_prerequisite.feat.name == "Feat 1"
    assert feat_skill_prerequisite.skill.name == "Coding"
