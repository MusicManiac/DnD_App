import pytest


@pytest.mark.django_db
def test_skill_creation(skill_fixture):
    skill = skill_fixture[0]
    assert skill.name == "Coding"
    assert skill.trained_only == False
    assert skill.armor_check_penalty == False
    assert skill.description == "Doing da thing"
    assert skill.link == "https://dontasktoask.com/"
    assert str(skill) == "Coding"
