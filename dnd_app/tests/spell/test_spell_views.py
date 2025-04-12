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
from tests.character_class_fixtures import character_class_fixture


@pytest.mark.django_db
def test_magic_aura_strength_list_view(client, magic_aura_strength_fixture):
    response = client.get("/api/spell/magic_aura_strength/")

    assert response.status_code == 200
    assert len(response.data) == len(magic_aura_strength_fixture)
    assert {mas["name"] for mas in response.data} == {
        mas.name for mas in magic_aura_strength_fixture
    }


@pytest.mark.django_db
def test_magic_aura_strength_create_view_success(client):
    data = {"name": "Very Strong", "description": "An extremely strong magic aura"}

    response = client.post("/api/spell/magic_aura_strength/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Very Strong"
    assert response.data["description"] == "An extremely strong magic aura"


@pytest.mark.django_db
def test_magic_aura_strength_create_view_fail(client, magic_aura_strength_fixture):
    data = {"name": "Weak", "description": "Weak magic aura"}

    response = client.post("/api/spell/magic_aura_strength/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "magic aura strength with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_magic_aura_strength_edit_view(client, magic_aura_strength_fixture):
    magic_aura_strength = magic_aura_strength_fixture[0]
    updated_data = {"name": "Updated Weak", "description": "Updated weak magic aura"}

    response = client.put(
        f"/api/spell/magic_aura_strength/{magic_aura_strength.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Weak"
    assert response.data["description"] == "Updated weak magic aura"


@pytest.mark.django_db
def test_magic_aura_strength_delete_view(client, magic_aura_strength_fixture):
    magic_aura_strength = magic_aura_strength_fixture[0]

    response = client.delete(
        f"/api/spell/magic_aura_strength/{magic_aura_strength.id}/"
    )

    assert response.status_code == 204
    assert not MagicAuraStrength.objects.filter(id=magic_aura_strength.id).exists()


@pytest.mark.django_db
def test_magic_school_list_view(client, magic_school_fixture):
    response = client.get("/api/spell/magic_schools/")

    assert response.status_code == 200
    assert len(response.data) == len(magic_school_fixture)
    assert {school["name"] for school in response.data} == {
        school.name for school in magic_school_fixture
    }


@pytest.mark.django_db
def test_magic_school_create_view_success(client):
    data = {"name": "Evocation", "description": "Evocation magic"}

    response = client.post("/api/spell/magic_schools/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Evocation"
    assert response.data["description"] == "Evocation magic"


@pytest.mark.django_db
def test_magic_school_create_view_fail(client, magic_school_fixture):
    data = {"name": "Abjuration", "description": "Abjuration magic"}

    response = client.post("/api/spell/magic_schools/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "magic school with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_magic_school_edit_view(client, magic_school_fixture):
    magic_school = magic_school_fixture[0]
    updated_data = {
        "name": "Updated Abjuration",
        "description": "Updated Abjuration magic",
    }

    response = client.put(
        f"/api/spell/magic_schools/{magic_school.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Abjuration"
    assert response.data["description"] == "Updated Abjuration magic"


@pytest.mark.django_db
def test_magic_school_delete_view(client, magic_school_fixture):
    magic_school = magic_school_fixture[0]

    response = client.delete(f"/api/spell/magic_schools/{magic_school.id}/")

    assert response.status_code == 204
    assert not MagicSchool.objects.filter(id=magic_school.id).exists()


@pytest.mark.django_db
def test_magic_subschool_list_view(client, magic_subschool_fixture):
    response = client.get("/api/spell/magic_subschools/")

    assert response.status_code == 200
    assert len(response.data) == len(magic_subschool_fixture)
    assert {subschool["name"] for subschool in response.data} == {
        subschool.name for subschool in magic_subschool_fixture
    }


@pytest.mark.django_db
def test_magic_subschool_create_view_success(client):
    data = {"name": "Evocation", "description": "Evocation magic"}

    response = client.post("/api/spell/magic_subschools/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Evocation"
    assert response.data["description"] == "Evocation magic"


@pytest.mark.django_db
def test_magic_subschool_create_view_fail(client, magic_subschool_fixture):
    data = {"name": "Teleportation", "description": "Teleportation magic"}

    response = client.post("/api/spell/magic_subschools/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "magic school with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_magic_subschool_edit_view(client, magic_subschool_fixture):
    magic_subschool = magic_subschool_fixture[0]
    updated_data = {
        "name": "Updated Teleportation",
        "description": "Updated teleportation magic",
    }

    response = client.put(
        f"/api/spell/magic_subschools/{magic_subschool.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Teleportation"
    assert response.data["description"] == "Updated teleportation magic"


@pytest.mark.django_db
def test_magic_subschool_delete_view(client, magic_subschool_fixture):
    magic_subschool = magic_subschool_fixture[0]

    response = client.delete(f"/api/spell/magic_subschools/{magic_subschool.id}/")

    assert response.status_code == 204
    assert not MagicSubSchool.objects.filter(id=magic_subschool.id).exists()


@pytest.mark.django_db
def test_spell_descriptor_list_view(client, spell_descriptor_fixture):
    response = client.get("/api/spell/spell_descriptors/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_descriptor_fixture)
    assert {descriptor["name"] for descriptor in response.data} == {
        descriptor.name for descriptor in spell_descriptor_fixture
    }


@pytest.mark.django_db
def test_spell_descriptor_create_view_success(client):
    data = {"name": "Water", "description": "Water magic"}

    response = client.post("/api/spell/spell_descriptors/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Water"
    assert response.data["description"] == "Water magic"


@pytest.mark.django_db
def test_spell_descriptor_create_view_fail(client, spell_descriptor_fixture):
    data = {"name": "Fire", "description": "Fire magic"}

    response = client.post("/api/spell/spell_descriptors/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "spell descriptor with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_spell_descriptor_edit_view(client, spell_descriptor_fixture):
    spell_descriptor = spell_descriptor_fixture[0]
    updated_data = {"name": "Updated Fire", "description": "Updated fire magic"}

    response = client.put(
        f"/api/spell/spell_descriptors/{spell_descriptor.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Fire"
    assert response.data["description"] == "Updated fire magic"


@pytest.mark.django_db
def test_spell_descriptor_delete_view(client, spell_descriptor_fixture):
    spell_descriptor = spell_descriptor_fixture[0]

    response = client.delete(f"/api/spell/spell_descriptors/{spell_descriptor.id}/")

    assert response.status_code == 204
    assert not SpellDescriptor.objects.filter(id=spell_descriptor.id).exists()


@pytest.mark.django_db
def test_spell_component_list_view(client, spell_component_fixture):
    response = client.get("/api/spell/spell_components/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_component_fixture)
    assert {component["name"] for component in response.data} == {
        component.name for component in spell_component_fixture
    }


@pytest.mark.django_db
def test_spell_component_create_view_success(client):
    data = {"name": "Divine", "short_name": "D", "description": "Divine component"}

    response = client.post("/api/spell/spell_components/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Divine"
    assert response.data["short_name"] == "D"
    assert response.data["description"] == "Divine component"


@pytest.mark.django_db
def test_spell_component_create_view_fail(client, spell_component_fixture):
    data = {"name": "Verbal", "short_name": "V", "description": "Verbal component"}

    response = client.post("/api/spell/spell_components/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "spell component with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_spell_component_edit_view(client, spell_component_fixture):
    spell_component = spell_component_fixture[0]
    updated_data = {
        "name": "Updated Verbal",
        "short_name": "V",
        "description": "Updated verbal component",
    }

    response = client.put(
        f"/api/spell/spell_components/{spell_component.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Verbal"
    assert response.data["description"] == "Updated verbal component"


@pytest.mark.django_db
def test_spell_component_delete_view(client, spell_component_fixture):
    spell_component = spell_component_fixture[0]

    response = client.delete(f"/api/spell/spell_components/{spell_component.id}/")

    assert response.status_code == 204
    assert not SpellComponent.objects.filter(id=spell_component.id).exists()


@pytest.mark.django_db
def test_casting_time_list_view(client, casting_time_fixture):
    response = client.get("/api/spell/casting_times/")

    assert response.status_code == 200
    assert len(response.data) == len(casting_time_fixture)
    assert {casting_time["name"] for casting_time in response.data} == {
        casting_time.name for casting_time in casting_time_fixture
    }


@pytest.mark.django_db
def test_casting_time_create_view_success(client):
    data = {"name": "Quick", "description": "Quick casting time"}

    response = client.post("/api/spell/casting_times/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Quick"
    assert response.data["description"] == "Quick casting time"


@pytest.mark.django_db
def test_casting_time_create_view_fail(client, casting_time_fixture):
    data = {"name": "Standard", "description": "Standard casting time"}

    response = client.post("/api/spell/casting_times/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "casting time with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_casting_time_edit_view(client, casting_time_fixture):
    casting_time = casting_time_fixture[0]
    updated_data = {
        "name": "Updated Standard",
        "description": "Updated standard casting time",
    }

    response = client.put(
        f"/api/spell/casting_times/{casting_time.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Standard"
    assert response.data["description"] == "Updated standard casting time"


@pytest.mark.django_db
def test_casting_time_delete_view(client, casting_time_fixture):
    casting_time = casting_time_fixture[0]

    response = client.delete(f"/api/spell/casting_times/{casting_time.id}/")

    assert response.status_code == 204
    assert not CastingTime.objects.filter(id=casting_time.id).exists()


@pytest.mark.django_db
def test_spell_range_list_view(client, spell_range_fixture):
    response = client.get("/api/spell/spell_ranges/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_range_fixture)
    assert {range["name"] for range in response.data} == {
        range.name for range in spell_range_fixture
    }


@pytest.mark.django_db
def test_spell_range_create_view_success(client):
    data = {"name": "Extreme", "description": "Extreme range"}

    response = client.post("/api/spell/spell_ranges/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Extreme"
    assert response.data["description"] == "Extreme range"


@pytest.mark.django_db
def test_spell_range_create_view_fail(client, spell_range_fixture):
    data = {"name": "Close", "description": "Close range"}

    response = client.post("/api/spell/spell_ranges/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "spell range with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_spell_range_edit_view(client, spell_range_fixture):
    spell_range = spell_range_fixture[0]
    updated_data = {"name": "Updated Close", "description": "Updated close range"}

    response = client.put(
        f"/api/spell/spell_ranges/{spell_range.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Close"
    assert response.data["description"] == "Updated close range"


@pytest.mark.django_db
def test_spell_range_delete_view(client, spell_range_fixture):
    spell_range = spell_range_fixture[0]

    response = client.delete(f"/api/spell/spell_ranges/{spell_range.id}/")

    assert response.status_code == 204
    assert not SpellRange.objects.filter(id=spell_range.id).exists()


@pytest.mark.django_db
def test_spell_list_view(client, spell_fixture):
    response = client.get("/api/spell/spells/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_fixture)
    assert {spell["name"] for spell in response.data} == {
        spell.name for spell in spell_fixture
    }


@pytest.fixture()
def self_containted_spell_level_fixture(
    spell_range_fixture,
    casting_time_fixture,
    magic_school_fixture,
    character_class_fixture,
):
    Spell.objects.create(
        name="Lightning Bolt",
        description="ZAP ZAP ZAP",
        school=magic_school_fixture[1],
        casting_time=casting_time_fixture[1],
        range=spell_range_fixture[1],
    )
    return [
        SpellLevel.objects.create(
            spell=Spell.objects.first(),
            character_class=character_class_fixture[0],
            level=3,
        )
    ]


@pytest.mark.django_db
def test_spell_create_view_success(
    client,
    magic_school_fixture,
    magic_subschool_fixture,
    casting_time_fixture,
    spell_range_fixture,
):
    data = {
        "id": 2222,
        "name": "Flame Strike",
        "description": "A fiery pillar",
        "link": "https://www.flamestrike.com",
        "target": "Point in space",
        "effect": "Fiery explosion",
        "area": "20 ft radius",
        "duration": "Instantaneous",
        "saving_throw": "Constitution",
        "spell_resistance": True,
        "school": magic_school_fixture[0].id,
        "subschool": magic_subschool_fixture[0].id,
        "casting_time": casting_time_fixture[0].id,
        "range": spell_range_fixture[0].id,
    }

    response = client.post("/api/spell/spells/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Flame Strike"
    assert response.data["description"] == "A fiery pillar"


@pytest.mark.django_db
def test_spell_create_view_fail(
    client,
    spell_fixture,
    magic_school_fixture,
    magic_subschool_fixture,
    casting_time_fixture,
    spell_range_fixture,
    spell_level_fixture,
):
    data = {
        "name": "Fireball",
        "description": "BIG BALL OF FOIRE",
        "school": magic_school_fixture[0].id,
        "casting_time": casting_time_fixture[0].id,
        "range": spell_range_fixture[0].id,
        "level": [spell_level_fixture[0].id],
    }

    response = client.post("/api/spell/spells/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "spell with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_spell_edit_view(
    client,
    spell_fixture,
    magic_school_fixture,
    magic_subschool_fixture,
    casting_time_fixture,
    spell_range_fixture,
):
    spell = spell_fixture[0]
    updated_data = {
        "name": "Updated Fireball",
        "description": "Updated description for the big fireball",
        "school": magic_school_fixture[0].id,
        "casting_time": casting_time_fixture[0].id,
        "range": spell_range_fixture[0].id,
    }

    response = client.put(f"/api/spell/spells/{spell.id}/", updated_data, format="json")

    print(SpellLevel.objects.all())
    print(response.data)
    assert response.status_code == 200
    assert response.data["name"] == "Updated Fireball"
    assert response.data["description"] == "Updated description for the big fireball"
    assert response.data["school"] == magic_school_fixture[0].id
    assert response.data["casting_time"] == casting_time_fixture[0].id
    assert response.data["range"] == spell_range_fixture[0].id


@pytest.mark.django_db
def test_spell_delete_view(client, spell_fixture):
    spell = spell_fixture[0]

    response = client.delete(f"/api/spell/spells/{spell.id}/")

    assert response.status_code == 204
    assert not Spell.objects.filter(id=spell.id).exists()


@pytest.mark.django_db
def test_spell_spell_descriptor_list_view(client, spell_spell_descriptor_fixture):
    response = client.get("/api/spell/spell_spell_descriptors/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_spell_descriptor_fixture)
    assert {ssd["spell"] for ssd in response.data} == {
        ssd.spell.id for ssd in spell_spell_descriptor_fixture
    }
    assert {ssd["descriptor"] for ssd in response.data} == {
        ssd.descriptor.id for ssd in spell_spell_descriptor_fixture
    }


@pytest.mark.django_db
def test_spell_spell_descriptor_create_view_success(
    client, spell_fixture, spell_descriptor_fixture
):
    data = {"spell": spell_fixture[0].id, "descriptor": spell_descriptor_fixture[0].id}

    response = client.post("/api/spell/spell_spell_descriptors/", data, format="json")

    assert response.status_code == 201
    assert response.data["spell"] == spell_fixture[0].id
    assert response.data["descriptor"] == spell_descriptor_fixture[0].id


@pytest.mark.django_db
def test_spell_spell_descriptor_create_view_fail(
    client, spell_spell_descriptor_fixture, spell_fixture, spell_descriptor_fixture
):
    data = {"spell": spell_fixture[0].id, "descriptor": spell_descriptor_fixture[0].id}

    response = client.post("/api/spell/spell_spell_descriptors/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields spell, descriptor must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_spell_spell_descriptor_edit_view(client, spell_spell_descriptor_fixture):
    spell_spell_descriptor = spell_spell_descriptor_fixture[0]
    updated_data = {
        "spell": spell_spell_descriptor.spell.id,
        "descriptor": spell_spell_descriptor.descriptor.id,
    }

    response = client.put(
        f"/api/spell/spell_spell_descriptors/{spell_spell_descriptor.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["spell"] == spell_spell_descriptor.spell.id
    assert response.data["descriptor"] == spell_spell_descriptor.descriptor.id


@pytest.mark.django_db
def test_spell_spell_descriptor_delete_view(client, spell_spell_descriptor_fixture):
    spell_spell_descriptor = spell_spell_descriptor_fixture[0]

    response = client.delete(
        f"/api/spell/spell_spell_descriptors/{spell_spell_descriptor.id}/"
    )

    assert response.status_code == 204
    assert not SpellSpellDescriptor.objects.filter(
        id=spell_spell_descriptor.id
    ).exists()


@pytest.mark.django_db
def test_spell_level_list_view(client, spell_level_fixture):
    response = client.get("/api/spell/spell_levels/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_level_fixture)
    assert {sl["spell"] for sl in response.data} == {
        sl.spell.id for sl in spell_level_fixture
    }
    assert {sl["character_class"] for sl in response.data} == {
        sl.character_class.id for sl in spell_level_fixture
    }
    assert {sl["level"] for sl in response.data} == {
        sl.level for sl in spell_level_fixture
    }


@pytest.mark.django_db
def test_spell_level_create_view_success(
    client, spell_fixture, character_class_fixture
):
    data = {
        "spell": spell_fixture[0].id,
        "character_class": character_class_fixture[0].id,
        "level": 4,
    }

    response = client.post("/api/spell/spell_levels/", data, format="json")

    assert response.status_code == 201
    assert response.data["spell"] == spell_fixture[0].id
    assert response.data["character_class"] == character_class_fixture[0].id
    assert response.data["level"] == 4


@pytest.mark.django_db
def test_spell_level_create_view_fail(
    client, spell_level_fixture, spell_fixture, character_class_fixture
):
    data = {
        "spell": spell_fixture[0].id,
        "character_class": character_class_fixture[0].id,
        "level": 3,
    }

    response = client.post("/api/spell/spell_levels/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields spell, character_class must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_spell_level_edit_view(client, spell_level_fixture):
    spell_level = spell_level_fixture[0]
    updated_data = {
        "spell": spell_level.spell.id,
        "character_class": spell_level.character_class.id,
        "level": 4,
    }

    response = client.put(
        f"/api/spell/spell_levels/{spell_level.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["level"] == 4


@pytest.mark.django_db
def test_spell_level_delete_view(client, spell_level_fixture):
    spell_level = spell_level_fixture[0]

    response = client.delete(f"/api/spell/spell_levels/{spell_level.id}/")

    assert response.status_code == 204
    assert not SpellLevel.objects.filter(id=spell_level.id).exists()


@pytest.mark.django_db
def test_spell_spell_component_list_view(client, spell_spell_component_fixture):
    response = client.get("/api/spell/spell_spell_components/")

    assert response.status_code == 200
    assert len(response.data) == len(spell_spell_component_fixture)
    assert {ssc["spell"] for ssc in response.data} == {
        ssc.spell.id for ssc in spell_spell_component_fixture
    }
    assert {ssc["component"] for ssc in response.data} == {
        ssc.component.id for ssc in spell_spell_component_fixture
    }


@pytest.mark.django_db
def test_spell_spell_component_create_view_success(
    client, spell_fixture, spell_component_fixture
):
    data = {"spell": spell_fixture[0].id, "component": spell_component_fixture[0].id}

    response = client.post("/api/spell/spell_spell_components/", data, format="json")

    assert response.status_code == 201
    assert response.data["spell"] == spell_fixture[0].id
    assert response.data["component"] == spell_component_fixture[0].id


@pytest.mark.django_db
def test_spell_spell_component_create_view_fail(
    client, spell_spell_component_fixture, spell_fixture, spell_component_fixture
):
    data = {
        "spell": spell_fixture[0].id,
        "component": spell_component_fixture[0].id,
    }

    response = client.post("/api/spell/spell_spell_components/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields spell, component must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_spell_spell_component_edit_view(client, spell_spell_component_fixture):
    spell_spell_component = spell_spell_component_fixture[0]
    updated_data = {
        "spell": spell_spell_component.spell.id,
        "component": spell_spell_component.component.id,
    }

    response = client.put(
        f"/api/spell/spell_spell_components/{spell_spell_component.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["spell"] == spell_spell_component.spell.id
    assert response.data["component"] == spell_spell_component.component.id


@pytest.mark.django_db
def test_spell_spell_component_delete_view(client, spell_spell_component_fixture):
    spell_spell_component = spell_spell_component_fixture[0]

    response = client.delete(
        f"/api/spell/spell_spell_components/{spell_spell_component.id}/"
    )

    assert response.status_code == 204
    assert not SpellSpellComponent.objects.filter(id=spell_spell_component.id).exists()
