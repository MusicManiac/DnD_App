import pytest

from item.models import (
    ItemCategory,
    Item,
    SpecialMaterial,
    WeaponMagicAbility,
    WeaponMagicAbilityFeat,
    WeaponMagicAbilitySpell,
    ArmorMagicAbility,
    ArmorMagicAbilityFeat,
    ArmorMagicAbilitySpell,
    WeaponCategory,
    WeaponDamageType,
    Weapon,
    WeaponWeaponCategory,
    WeaponWeaponDamageType,
    WeaponWeaponMagicAbility,
    ArmorType,
    Armor,
    ArmorArmorMagicAbility,
)


@pytest.mark.django_db
def test_item_category_list_view(client, item_category_fixture):
    response = client.get("/api/item/item_category/")

    assert response.status_code == 200
    assert len(response.data) == len(item_category_fixture)
    assert {category["name"] for category in response.data} == {
        "Pain",
        "Suffering",
        "TestCategory",
    }


@pytest.mark.django_db
def test_item_category_create_view_success(client):
    data = {"name": "Healing", "description": "Healing items category"}

    response = client.post("/api/item/item_category/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Healing"
    assert response.data["description"] == "Healing items category"


@pytest.mark.django_db
def test_item_category_create_view_fail(client, item_category_fixture):
    data = {
        "name": "Pain",
    }

    response = client.post("/api/item/item_category/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "item category with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_item_category_edit_view(client, item_category_fixture):
    item_category = item_category_fixture[0]
    updated_data = {
        "name": "Updated Pain",
        "description": "Updated description for Pain category",
    }

    response = client.put(
        f"/api/item/item_category/{item_category.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Pain"
    assert response.data["description"] == "Updated description for Pain category"


@pytest.mark.django_db
def test_item_category_delete_view(client, item_category_fixture):
    item_category = item_category_fixture[0]

    response = client.delete(f"/api/item/item_category/{item_category.id}/")

    assert response.status_code == 204
    assert not ItemCategory.objects.filter(id=item_category.id).exists()


@pytest.mark.django_db
def test_item_list_view(client, item_fixture):
    response = client.get("/api/item/item/")

    assert response.status_code == 200
    assert len(response.data) == len(item_fixture)
    assert {item["name"] for item in response.data} == {"Cookie", "Keyboard"}


@pytest.mark.django_db
def test_item_create_view_success(client, item_category_fixture):
    data = {
        "name": "Sword",
        "description": "A sharp sword",
        "weight_in_lb": 3.50,
        "price_in_gp": 50.00,
        "hardness": 20,
        "hit_points": 50,
        "category": item_category_fixture[0].id,
    }

    response = client.post("/api/item/item/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Sword"
    assert response.data["description"] == "A sharp sword"
    assert response.data["weight_in_lb"] == "3.50"


@pytest.mark.django_db
def test_item_create_view_fail(client, item_fixture, item_category_fixture):
    data = {
        "name": "Cookie",
        "description": "Omnonomnom",
        "weight_in_lb": 5.5,
        "price_in_gp": 150.00,
        "hardness": 10,
        "hit_points": 20,
        "category": item_category_fixture[0].id,
    }

    response = client.post("/api/item/item/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "item with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_item_edit_view(client, item_fixture):
    item = item_fixture[0]
    updated_data = {
        "name": "Updated Cookie",
        "description": "Updated omnonomnom",
        "weight_in_lb": 5.0,
        "price_in_gp": 160.00,
        "hardness": 12,
        "hit_points": 22,
        "category": item.category.id,
    }

    response = client.put(f"/api/item/item/{item.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Cookie"
    assert response.data["description"] == "Updated omnonomnom"


@pytest.mark.django_db
def test_item_delete_view(client, item_fixture):
    item = item_fixture[0]

    response = client.delete(f"/api/item/item/{item.id}/")

    assert response.status_code == 204
    assert not Item.objects.filter(id=item.id).exists()


@pytest.mark.django_db
def test_special_material_list_view(client, special_material_fixture):
    response = client.get("/api/item/special_material/")

    assert response.status_code == 200
    assert len(response.data) == len(special_material_fixture)
    assert {material["name"] for material in response.data} == {"Adamantine", "Mithral"}


@pytest.mark.django_db
def test_special_material_create_view_success(client):
    data = {
        "name": "Dragonbone",
        "description": "Dragonbone material used for crafting powerful items.",
        "link": "https://www.dragonbone.com",
    }

    response = client.post("/api/item/special_material/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Dragonbone"
    assert (
        response.data["description"]
        == "Dragonbone material used for crafting powerful items."
    )
    assert response.data["link"] == "https://www.dragonbone.com"


@pytest.mark.django_db
def test_special_material_create_view_fail(client, special_material_fixture):
    data = {
        "name": "Adamantine",
        "description": "A very hard and durable material.",
        "link": "http://adamantine.com",
    }

    response = client.post("/api/item/special_material/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "special material with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_special_material_edit_view(client, special_material_fixture):
    special_material = special_material_fixture[0]
    updated_data = {
        "name": "Updated Adamantine",
        "description": "Updated description for Adamantine material.",
        "link": "https://www.updatedadamantine.com",
    }

    response = client.put(
        f"/api/item/special_material/{special_material.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Adamantine"
    assert (
        response.data["description"] == "Updated description for Adamantine material."
    )
    assert response.data["link"] == "https://www.updatedadamantine.com"


@pytest.mark.django_db
def test_special_material_delete_view(client, special_material_fixture):
    special_material = special_material_fixture[0]

    response = client.delete(f"/api/item/special_material/{special_material.id}/")

    assert response.status_code == 204
    assert not SpecialMaterial.objects.filter(id=special_material.id).exists()


@pytest.mark.django_db
def test_weapon_magic_ability_list_view(client, weapon_magic_ability_fixture):
    response = client.get("/api/item/weapon_magic_ability/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_magic_ability_fixture)
    assert {wma["name"] for wma in response.data} == {"Flaming", "Frost", "Frost222"}


@pytest.mark.django_db
def test_weapon_magic_ability_create_view_success(
    client, magic_aura_strength_fixture, magic_school_fixture
):
    data = {
        "name": "Burning",
        "description": "Adds fire damage over time.",
        "caster_level_required_for_creation": 10,
        "other_craft_requirements": "Requires crafter to meditate for 1 hour.",
        "cost_increase_in_bonus": 1,
        "magic_aura_strength": magic_aura_strength_fixture[0].id,
        "magic_aura_type": magic_school_fixture[0].id,
    }

    response = client.post("/api/item/weapon_magic_ability/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Burning"
    assert response.data["description"] == "Adds fire damage over time."
    assert response.data["cost_increase_in_bonus"] == 1


@pytest.mark.django_db
def test_weapon_magic_ability_create_view_fail(
    client,
    weapon_magic_ability_fixture,
    magic_aura_strength_fixture,
    magic_school_fixture,
):
    data = {
        "name": "Flaming",
        "description": "Adds fire damage to attacks.",
        "caster_level_required_for_creation": 10,
        "other_craft_requirements": "Requires crafter to watch LOTR at least 5 times",
        "cost_increase_in_bonus": 1,
        "magic_aura_strength": magic_aura_strength_fixture[0].id,
        "magic_aura_type": magic_school_fixture[0].id,
    }

    response = client.post("/api/item/weapon_magic_ability/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert (
        "weapon magic ability with this name already exists." in response.data["name"]
    )


@pytest.mark.django_db
def test_weapon_magic_ability_edit_view(client, weapon_magic_ability_fixture):
    weapon_magic_ability = weapon_magic_ability_fixture[0]
    updated_data = {
        "name": "Updated Flaming",
        "description": "Updated fire damage",
        "caster_level_required_for_creation": 12,
        "other_craft_requirements": "Requires crafter to meditate for 2 hours.",
        "cost_increase_in_bonus": 2,
        "magic_aura_strength": weapon_magic_ability.magic_aura_strength.id,
        "magic_aura_type": weapon_magic_ability.magic_aura_type.id,
    }

    response = client.put(
        f"/api/item/weapon_magic_ability/{weapon_magic_ability.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Flaming"
    assert response.data["description"] == "Updated fire damage"
    assert response.data["cost_increase_in_bonus"] == 2


@pytest.mark.django_db
def test_weapon_magic_ability_delete_view(client, weapon_magic_ability_fixture):
    weapon_magic_ability = weapon_magic_ability_fixture[0]

    response = client.delete(
        f"/api/item/weapon_magic_ability/{weapon_magic_ability.id}/"
    )

    assert response.status_code == 204
    assert not WeaponMagicAbility.objects.filter(id=weapon_magic_ability.id).exists()


@pytest.mark.django_db
def test_weapon_magic_ability_feat_list_view(client, weapon_magic_ability_feat_fixture):
    response = client.get("/api/item/weapon_magic_ability_feat/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_magic_ability_feat_fixture)
    assert {wmf["weapon_magic_ability"] for wmf in response.data} == {
        wmf.weapon_magic_ability.id for wmf in weapon_magic_ability_feat_fixture
    }
    assert {wmf["feat"] for wmf in response.data} == {
        wmf.feat.id for wmf in weapon_magic_ability_feat_fixture
    }


@pytest.mark.django_db
def test_weapon_magic_ability_feat_create_view_success(
    client, weapon_magic_ability_fixture, feat_fixture
):
    data = {
        "weapon_magic_ability": weapon_magic_ability_fixture[0].id,
        "feat": feat_fixture[0].id,
    }

    response = client.post("/api/item/weapon_magic_ability_feat/", data, format="json")

    assert response.status_code == 201
    assert response.data["weapon_magic_ability"] == weapon_magic_ability_fixture[0].id
    assert response.data["feat"] == feat_fixture[0].id


@pytest.mark.django_db
def test_weapon_magic_ability_feat_create_view_fail(
    client,
    weapon_magic_ability_feat_fixture,
    weapon_magic_ability_fixture,
    feat_fixture,
):
    data = {
        "weapon_magic_ability": weapon_magic_ability_fixture[0].id,
        "feat": feat_fixture[0].id,
    }

    response = client.post("/api/item/weapon_magic_ability_feat/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields weapon_magic_ability, feat must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_weapon_magic_ability_feat_edit_view(client, weapon_magic_ability_feat_fixture):
    weapon_magic_ability_feat = weapon_magic_ability_feat_fixture[0]
    updated_data = {
        "weapon_magic_ability": weapon_magic_ability_feat.weapon_magic_ability.id,
        "feat": weapon_magic_ability_feat.feat.id,
    }

    response = client.put(
        f"/api/item/weapon_magic_ability_feat/{weapon_magic_ability_feat.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert (
        response.data["weapon_magic_ability"]
        == weapon_magic_ability_feat.weapon_magic_ability.id
    )
    assert response.data["feat"] == weapon_magic_ability_feat.feat.id


@pytest.mark.django_db
def test_weapon_magic_ability_feat_delete_view(
    client, weapon_magic_ability_feat_fixture
):
    weapon_magic_ability_feat = weapon_magic_ability_feat_fixture[0]

    response = client.delete(
        f"/api/item/weapon_magic_ability_feat/{weapon_magic_ability_feat.id}/"
    )

    assert response.status_code == 204
    assert not WeaponMagicAbilityFeat.objects.filter(
        id=weapon_magic_ability_feat.id
    ).exists()


@pytest.mark.django_db
def test_weapon_magic_ability_spell_list_view(
    client, weapon_magic_ability_spell_fixture
):
    response = client.get("/api/item/weapon_magic_ability_spell/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_magic_ability_spell_fixture)
    assert {wmas["weapon_magic_ability"] for wmas in response.data} == {
        wmas.weapon_magic_ability.id for wmas in weapon_magic_ability_spell_fixture
    }
    assert {wmas["spell"] for wmas in response.data} == {
        wmas.spell.id for wmas in weapon_magic_ability_spell_fixture
    }


@pytest.mark.django_db
def test_weapon_magic_ability_spell_create_view_success(
    client, weapon_magic_ability_fixture, spell_fixture
):
    data = {
        "weapon_magic_ability": weapon_magic_ability_fixture[0].id,
        "spell": spell_fixture[0].id,
    }

    response = client.post("/api/item/weapon_magic_ability_spell/", data, format="json")

    assert response.status_code == 201
    assert response.data["weapon_magic_ability"] == weapon_magic_ability_fixture[0].id
    assert response.data["spell"] == spell_fixture[0].id


@pytest.mark.django_db
def test_weapon_magic_ability_spell_create_view_fail(
    client,
    weapon_magic_ability_spell_fixture,
    weapon_magic_ability_fixture,
    spell_fixture,
):
    data = {
        "weapon_magic_ability": weapon_magic_ability_fixture[0].id,
        "spell": spell_fixture[0].id,
    }

    response = client.post("/api/item/weapon_magic_ability_spell/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields weapon_magic_ability, spell must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_weapon_magic_ability_spell_edit_view(
    client, weapon_magic_ability_spell_fixture
):
    weapon_magic_ability_spell = weapon_magic_ability_spell_fixture[0]
    updated_data = {
        "weapon_magic_ability": weapon_magic_ability_spell.weapon_magic_ability.id,
        "spell": weapon_magic_ability_spell.spell.id,
    }

    response = client.put(
        f"/api/item/weapon_magic_ability_spell/{weapon_magic_ability_spell.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert (
        response.data["weapon_magic_ability"]
        == weapon_magic_ability_spell.weapon_magic_ability.id
    )
    assert response.data["spell"] == weapon_magic_ability_spell.spell.id


@pytest.mark.django_db
def test_weapon_magic_ability_spell_delete_view(
    client, weapon_magic_ability_spell_fixture
):
    weapon_magic_ability_spell = weapon_magic_ability_spell_fixture[0]

    response = client.delete(
        f"/api/item/weapon_magic_ability_spell/{weapon_magic_ability_spell.id}/"
    )

    assert response.status_code == 204
    assert not WeaponMagicAbilitySpell.objects.filter(
        id=weapon_magic_ability_spell.id
    ).exists()


@pytest.mark.django_db
def test_armor_magic_ability_list_view(client, armor_magic_ability_fixture):
    response = client.get("/api/item/armor_magic_ability/")

    assert response.status_code == 200
    assert len(response.data) == len(armor_magic_ability_fixture)
    assert {ama["name"] for ama in response.data} == {"Fortification", "Shadow"}


@pytest.mark.django_db
def test_armor_magic_ability_create_view_success(
    client, magic_aura_strength_fixture, magic_school_fixture
):
    data = {
        "name": "Improved Fortification",
        "description": "Enhances the fortification properties.",
        "caster_level_required_for_creation": 15,
        "cost_increase_in_bonus": 4,
        "magic_aura_strength": magic_aura_strength_fixture[2].id,
        "magic_aura_type": magic_school_fixture[1].id,
    }

    response = client.post("/api/item/armor_magic_ability/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Improved Fortification"
    assert response.data["description"] == "Enhances the fortification properties."
    assert response.data["cost_increase_in_bonus"] == 4


@pytest.mark.django_db
def test_armor_magic_ability_create_view_fail(
    client,
    armor_magic_ability_fixture,
    magic_aura_strength_fixture,
    magic_school_fixture,
):
    data = {
        "name": "Fortification",
        "description": "Provides a chance to negate critical hits.",
        "caster_level_required_for_creation": 13,
        "cost_increase_in_bonus": 3,
        "magic_aura_strength": magic_aura_strength_fixture[2].id,
        "magic_aura_type": magic_school_fixture[1].id,
    }

    response = client.post("/api/item/armor_magic_ability/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "armor magic ability with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_armor_magic_ability_edit_view(client, armor_magic_ability_fixture):
    armor_magic_ability = armor_magic_ability_fixture[0]
    updated_data = {
        "name": "Updated Fortification",
        "description": "Updated description for fortification ability",
        "caster_level_required_for_creation": 14,
        "cost_increase_in_bonus": 5,
        "magic_aura_strength": armor_magic_ability.magic_aura_strength.id,
        "magic_aura_type": armor_magic_ability.magic_aura_type.id,
    }

    response = client.put(
        f"/api/item/armor_magic_ability/{armor_magic_ability.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Fortification"
    assert (
        response.data["description"] == "Updated description for fortification ability"
    )
    assert response.data["cost_increase_in_bonus"] == 5


@pytest.mark.django_db
def test_armor_magic_ability_delete_view(client, armor_magic_ability_fixture):
    armor_magic_ability = armor_magic_ability_fixture[0]

    response = client.delete(f"/api/item/armor_magic_ability/{armor_magic_ability.id}/")

    assert response.status_code == 204
    assert not ArmorMagicAbility.objects.filter(id=armor_magic_ability.id).exists()


@pytest.mark.django_db
def test_armor_magic_ability_feat_list_view(client, armor_magic_ability_feat_fixture):
    response = client.get("/api/item/armor_magic_ability_feat/")

    assert response.status_code == 200
    assert len(response.data) == len(armor_magic_ability_feat_fixture)
    assert {amaf["armor_magic_ability"] for amaf in response.data} == {
        amaf.armor_magic_ability.id for amaf in armor_magic_ability_feat_fixture
    }
    assert {amaf["feat"] for amaf in response.data} == {
        amaf.feat.id for amaf in armor_magic_ability_feat_fixture
    }


@pytest.mark.django_db
def test_armor_magic_ability_feat_create_view_success(
    client, armor_magic_ability_fixture, feat_fixture
):
    data = {
        "armor_magic_ability": armor_magic_ability_fixture[0].id,
        "feat": feat_fixture[0].id,
    }

    response = client.post("/api/item/armor_magic_ability_feat/", data, format="json")

    assert response.status_code == 201
    assert response.data["armor_magic_ability"] == armor_magic_ability_fixture[0].id
    assert response.data["feat"] == feat_fixture[0].id


@pytest.mark.django_db
def test_armor_magic_ability_feat_create_view_fail(
    client, armor_magic_ability_feat_fixture, armor_magic_ability_fixture, feat_fixture
):
    data = {
        "armor_magic_ability": armor_magic_ability_fixture[0].id,
        "feat": feat_fixture[0].id,
    }

    response = client.post("/api/item/armor_magic_ability_feat/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields armor_magic_ability, feat must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_armor_magic_ability_feat_edit_view(client, armor_magic_ability_feat_fixture):
    armor_magic_ability_feat = armor_magic_ability_feat_fixture[0]
    updated_data = {
        "armor_magic_ability": armor_magic_ability_feat.armor_magic_ability.id,
        "feat": armor_magic_ability_feat.feat.id,
    }

    response = client.put(
        f"/api/item/armor_magic_ability_feat/{armor_magic_ability_feat.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert (
        response.data["armor_magic_ability"]
        == armor_magic_ability_feat.armor_magic_ability.id
    )
    assert response.data["feat"] == armor_magic_ability_feat.feat.id


@pytest.mark.django_db
def test_armor_magic_ability_feat_delete_view(client, armor_magic_ability_feat_fixture):
    armor_magic_ability_feat = armor_magic_ability_feat_fixture[0]

    response = client.delete(
        f"/api/item/armor_magic_ability_feat/{armor_magic_ability_feat.id}/"
    )

    assert response.status_code == 204
    assert not ArmorMagicAbilityFeat.objects.filter(
        id=armor_magic_ability_feat.id
    ).exists()


@pytest.mark.django_db
def test_armor_magic_ability_spell_list_view(client, armor_magic_ability_spell_fixture):
    response = client.get("/api/item/armor_magic_ability_spell/")

    assert response.status_code == 200
    assert len(response.data) == len(armor_magic_ability_spell_fixture)
    assert {ams["armor_magic_ability"] for ams in response.data} == {
        ams.armor_magic_ability.id for ams in armor_magic_ability_spell_fixture
    }
    assert {ams["spell"] for ams in response.data} == {
        ams.spell.id for ams in armor_magic_ability_spell_fixture
    }


@pytest.mark.django_db
def test_armor_magic_ability_spell_create_view_success(
    client, armor_magic_ability_fixture, spell_fixture
):
    data = {
        "armor_magic_ability": armor_magic_ability_fixture[0].id,
        "spell": spell_fixture[0].id,
    }

    response = client.post("/api/item/armor_magic_ability_spell/", data, format="json")

    assert response.status_code == 201
    assert response.data["armor_magic_ability"] == armor_magic_ability_fixture[0].id
    assert response.data["spell"] == spell_fixture[0].id


@pytest.mark.django_db
def test_armor_magic_ability_spell_create_view_fail(
    client,
    armor_magic_ability_spell_fixture,
    armor_magic_ability_fixture,
    spell_fixture,
):
    data = {
        "armor_magic_ability": armor_magic_ability_fixture[0].id,
        "spell": spell_fixture[0].id,
    }

    response = client.post("/api/item/armor_magic_ability_spell/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields armor_magic_ability, spell must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_armor_magic_ability_spell_edit_view(client, armor_magic_ability_spell_fixture):
    armor_magic_ability_spell = armor_magic_ability_spell_fixture[0]
    updated_data = {
        "armor_magic_ability": armor_magic_ability_spell.armor_magic_ability.id,
        "spell": armor_magic_ability_spell.spell.id,
    }

    response = client.put(
        f"/api/item/armor_magic_ability_spell/{armor_magic_ability_spell.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert (
        response.data["armor_magic_ability"]
        == armor_magic_ability_spell.armor_magic_ability.id
    )
    assert response.data["spell"] == armor_magic_ability_spell.spell.id


@pytest.mark.django_db
def test_armor_magic_ability_spell_delete_view(
    client, armor_magic_ability_spell_fixture
):
    armor_magic_ability_spell = armor_magic_ability_spell_fixture[0]

    response = client.delete(
        f"/api/item/armor_magic_ability_spell/{armor_magic_ability_spell.id}/"
    )

    assert response.status_code == 204
    assert not ArmorMagicAbilitySpell.objects.filter(
        id=armor_magic_ability_spell.id
    ).exists()


@pytest.mark.django_db
def test_weapon_category_list_view(client, weapon_category_fixture):
    response = client.get("/api/item/weapon_category/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_category_fixture)
    assert {category["name"] for category in response.data} == {
        "Simple",
        "Martial",
        "Exotic",
    }


@pytest.mark.django_db
def test_weapon_category_create_view_success(client):
    data = {
        "name": "Heavy",
        "description": "Weapons that require significant strength to wield.",
    }

    response = client.post("/api/item/weapon_category/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Heavy"
    assert (
        response.data["description"]
        == "Weapons that require significant strength to wield."
    )


@pytest.mark.django_db
def test_weapon_category_create_view_fail(client, weapon_category_fixture):
    data = {
        "name": "Simple",
        "description": "Basic weapons that require minimal training.",
    }

    response = client.post("/api/item/weapon_category/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "weapon category with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_weapon_category_edit_view(client, weapon_category_fixture):
    weapon_category = weapon_category_fixture[0]
    updated_data = {
        "name": "Updated Simple",
        "description": "Updated description for basic weapons.",
    }

    response = client.put(
        f"/api/item/weapon_category/{weapon_category.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Simple"
    assert response.data["description"] == "Updated description for basic weapons."


@pytest.mark.django_db
def test_weapon_category_delete_view(client, weapon_category_fixture):
    weapon_category = weapon_category_fixture[0]

    response = client.delete(f"/api/item/weapon_category/{weapon_category.id}/")

    assert response.status_code == 204
    assert not WeaponCategory.objects.filter(id=weapon_category.id).exists()


@pytest.mark.django_db
def test_weapon_damage_type_list_view(client, weapon_damage_type_fixture):
    response = client.get("/api/item/weapon_damage_type/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_damage_type_fixture)
    assert {wdt["name"] for wdt in response.data} == {
        "Bludgeoning",
        "Piercing",
        "Slashing",
    }


@pytest.mark.django_db
def test_weapon_damage_type_create_view_success(client):
    data = {"name": "Crushing", "description": "Crushing damage"}

    response = client.post("/api/item/weapon_damage_type/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Crushing"
    assert response.data["description"] == "Crushing damage"


@pytest.mark.django_db
def test_weapon_damage_type_create_view_fail(client, weapon_damage_type_fixture):
    data = {"name": "Bludgeoning", "description": "Smashing"}

    response = client.post("/api/item/weapon_damage_type/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "weapon damage type with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_weapon_damage_type_edit_view(client, weapon_damage_type_fixture):
    weapon_damage_type = weapon_damage_type_fixture[0]
    updated_data = {
        "name": "Updated Bludgeoning",
        "description": "Updated smashing damage",
    }

    response = client.put(
        f"/api/item/weapon_damage_type/{weapon_damage_type.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Bludgeoning"
    assert response.data["description"] == "Updated smashing damage"


@pytest.mark.django_db
def test_weapon_damage_type_delete_view(client, weapon_damage_type_fixture):
    weapon_damage_type = weapon_damage_type_fixture[0]

    response = client.delete(f"/api/item/weapon_damage_type/{weapon_damage_type.id}/")

    assert response.status_code == 204
    assert not WeaponDamageType.objects.filter(id=weapon_damage_type.id).exists()


@pytest.mark.django_db
def test_weapon_list_view(client, weapon_fixture):
    response = client.get("/api/item/weapon/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_fixture)
    assert {weapon["name"] for weapon in response.data} == {
        "Longsword full properties",
        "Longsword",
        "warhammer",
    }


@pytest.mark.django_db
def test_weapon_create_view_success(
    client, weapon_damage_type_fixture, special_material_fixture, item_category_fixture
):
    data = {
        "name": "Battleaxe",
        "description": "A powerful axe.",
        "category": item_category_fixture[0].id,
        "weight_in_lb": 6.0,
        "price_in_gp": 200.00,
        "hardness": 12,
        "hit_points": 30,
        "damage": "1d10",
        "crit_multiplier": 3,
        "crit_range": "20",
        "range_increment_in_ft": 30,
        "is_masterwork": False,
        "enchantment_bonus": 2,
        "special_material": special_material_fixture[0].id,
        "weapon_damage_type": weapon_damage_type_fixture[0].id,
    }

    response = client.post("/api/item/weapon/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Battleaxe"
    assert response.data["description"] == "A powerful axe."
    assert response.data["price_in_gp"] == "200.00"


@pytest.mark.django_db
def test_weapon_create_view_fail(
    client,
    weapon_fixture,
    weapon_damage_type_fixture,
    special_material_fixture,
    item_category_fixture,
):
    data = {
        "name": "Longsword full properties",
        "description": "A versatile sword.",
        "category": item_category_fixture[0].id,
        "weight_in_lb": 5.5,
        "price_in_gp": 150.00,
        "hardness": 10,
        "hit_points": 20,
        "damage": "1d8",
        "crit_multiplier": 2,
        "crit_range": "19-20",
        "range_increment_in_ft": 20,
        "is_masterwork": True,
        "enchantment_bonus": 1,
        "special_material": special_material_fixture[0].id,
        "weapon_damage_type": weapon_damage_type_fixture[0].id,
    }

    response = client.post("/api/item/weapon/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "item with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_weapon_edit_view(client, weapon_fixture):
    weapon = weapon_fixture[0]
    updated_data = {
        "name": "Updated Longsword",
        "description": "An updated versatile sword.",
        "category": weapon.category.id,
        "weight_in_lb": 5.0,
        "price_in_gp": 175.00,
        "hardness": 12,
        "hit_points": 25,
        "damage": "1d8",
        "crit_multiplier": 2,
        "crit_range": "19-20",
        "range_increment_in_ft": 20,
        "is_masterwork": False,
        "enchantment_bonus": 1,
        "special_material": weapon.special_material.id,
        "weapon_damage_type": weapon.weapon_damage_type.id,
    }

    response = client.put(f"/api/item/weapon/{weapon.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Longsword"
    assert response.data["description"] == "An updated versatile sword."


@pytest.mark.django_db
def test_weapon_delete_view(client, weapon_fixture):
    weapon = weapon_fixture[0]

    response = client.delete(f"/api/item/weapon/{weapon.id}/")

    assert response.status_code == 204
    assert not Weapon.objects.filter(id=weapon.id).exists()


@pytest.mark.django_db
def test_weapon_weapon_category_list_view(client, weapon_weapon_category_fixture):
    response = client.get("/api/item/weapon_weapon_category/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_weapon_category_fixture)
    assert {wwc["weapon"] for wwc in response.data} == {
        wwc.weapon.id for wwc in weapon_weapon_category_fixture
    }
    assert {wwc["weapon_category"] for wwc in response.data} == {
        wwc.weapon_category.id for wwc in weapon_weapon_category_fixture
    }


@pytest.mark.django_db
def test_weapon_weapon_category_create_view_success(
    client, weapon_fixture, weapon_category_fixture
):
    data = {
        "weapon": weapon_fixture[0].id,
        "weapon_category": weapon_category_fixture[0].id,
    }

    response = client.post("/api/item/weapon_weapon_category/", data, format="json")

    assert response.status_code == 201
    assert response.data["weapon"] == weapon_fixture[0].id
    assert response.data["weapon_category"] == weapon_category_fixture[0].id


@pytest.mark.django_db
def test_weapon_weapon_category_create_view_fail(
    client, weapon_weapon_category_fixture, weapon_fixture, weapon_category_fixture
):
    data = {
        "weapon": weapon_fixture[0].id,
        "weapon_category": weapon_category_fixture[0].id,
    }

    response = client.post("/api/item/weapon_weapon_category/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields weapon, weapon_category must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_weapon_weapon_category_edit_view(client, weapon_weapon_category_fixture):
    weapon_weapon_category = weapon_weapon_category_fixture[0]
    updated_data = {
        "weapon": weapon_weapon_category.weapon.id,
        "weapon_category": weapon_weapon_category.weapon_category.id,
    }

    response = client.put(
        f"/api/item/weapon_weapon_category/{weapon_weapon_category.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["weapon"] == weapon_weapon_category.weapon.id
    assert response.data["weapon_category"] == weapon_weapon_category.weapon_category.id


@pytest.mark.django_db
def test_weapon_weapon_category_delete_view(client, weapon_weapon_category_fixture):
    weapon_weapon_category = weapon_weapon_category_fixture[0]

    response = client.delete(
        f"/api/item/weapon_weapon_category/{weapon_weapon_category.id}/"
    )

    assert response.status_code == 204
    assert not WeaponWeaponCategory.objects.filter(
        id=weapon_weapon_category.id
    ).exists()


@pytest.mark.django_db
def test_weapon_weapon_damage_type_list_view(client, weapon_weapon_damage_type_fixture):
    response = client.get("/api/item/weapon_weapon_damage_type/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_weapon_damage_type_fixture)
    assert {wwdt["weapon"] for wwdt in response.data} == {
        wwdt.weapon.id for wwdt in weapon_weapon_damage_type_fixture
    }
    assert {wwdt["weapon_damage_type"] for wwdt in response.data} == {
        wwdt.weapon_damage_type.id for wwdt in weapon_weapon_damage_type_fixture
    }


@pytest.mark.django_db
def test_weapon_weapon_damage_type_create_view_success(
    client, weapon_fixture, weapon_damage_type_fixture
):
    data = {
        "weapon": weapon_fixture[0].id,
        "weapon_damage_type": weapon_damage_type_fixture[0].id,
    }

    response = client.post("/api/item/weapon_weapon_damage_type/", data, format="json")

    assert response.status_code == 201
    assert response.data["weapon"] == weapon_fixture[0].id
    assert response.data["weapon_damage_type"] == weapon_damage_type_fixture[0].id


@pytest.mark.django_db
def test_weapon_weapon_damage_type_create_view_fail(
    client,
    weapon_weapon_damage_type_fixture,
    weapon_fixture,
    weapon_damage_type_fixture,
):
    data = {
        "weapon": weapon_fixture[0].id,
        "weapon_damage_type": weapon_damage_type_fixture[0].id,
    }

    response = client.post("/api/item/weapon_weapon_damage_type/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields weapon, weapon_damage_type must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_weapon_weapon_damage_type_edit_view(client, weapon_weapon_damage_type_fixture):
    weapon_weapon_damage_type = weapon_weapon_damage_type_fixture[0]
    updated_data = {
        "weapon": weapon_weapon_damage_type.weapon.id,
        "weapon_damage_type": weapon_weapon_damage_type.weapon_damage_type.id,
    }

    response = client.put(
        f"/api/item/weapon_weapon_damage_type/{weapon_weapon_damage_type.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["weapon"] == weapon_weapon_damage_type.weapon.id
    assert (
        response.data["weapon_damage_type"]
        == weapon_weapon_damage_type.weapon_damage_type.id
    )


@pytest.mark.django_db
def test_weapon_weapon_damage_type_delete_view(
    client, weapon_weapon_damage_type_fixture
):
    weapon_weapon_damage_type = weapon_weapon_damage_type_fixture[0]

    response = client.delete(
        f"/api/item/weapon_weapon_damage_type/{weapon_weapon_damage_type.id}/"
    )

    assert response.status_code == 204
    assert not WeaponWeaponDamageType.objects.filter(
        id=weapon_weapon_damage_type.id
    ).exists()


@pytest.mark.django_db
def test_weapon_weapon_magic_ability_list_view(
    client, weapon_weapon_magic_ability_fixture
):
    response = client.get("/api/item/weapon_weapon_magic_ability/")

    assert response.status_code == 200
    assert len(response.data) == len(weapon_weapon_magic_ability_fixture)
    assert {wwma["weapon"] for wwma in response.data} == {
        wwma.weapon.id for wwma in weapon_weapon_magic_ability_fixture
    }
    assert {wwma["weapon_magic_ability"] for wwma in response.data} == {
        wwma.weapon_magic_ability.id for wwma in weapon_weapon_magic_ability_fixture
    }


@pytest.mark.django_db
def test_weapon_weapon_magic_ability_create_view_success(
    client, weapon_fixture, weapon_magic_ability_fixture
):
    data = {
        "weapon": weapon_fixture[0].id,
        "weapon_magic_ability": weapon_magic_ability_fixture[0].id,
    }

    response = client.post(
        "/api/item/weapon_weapon_magic_ability/", data, format="json"
    )

    assert response.status_code == 201
    assert response.data["weapon"] == weapon_fixture[0].id
    assert response.data["weapon_magic_ability"] == weapon_magic_ability_fixture[0].id


@pytest.mark.django_db
def test_weapon_weapon_magic_ability_create_view_fail(
    client,
    weapon_weapon_magic_ability_fixture,
    weapon_fixture,
    weapon_magic_ability_fixture,
):
    data = {
        "weapon": weapon_fixture[0].id,
        "weapon_magic_ability": weapon_magic_ability_fixture[0].id,
    }

    response = client.post(
        "/api/item/weapon_weapon_magic_ability/", data, format="json"
    )

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields weapon, weapon_magic_ability must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_weapon_weapon_magic_ability_edit_view(
    client, weapon_weapon_magic_ability_fixture
):
    weapon_weapon_magic_ability = weapon_weapon_magic_ability_fixture[0]
    updated_data = {
        "weapon": weapon_weapon_magic_ability.weapon.id,
        "weapon_magic_ability": weapon_weapon_magic_ability.weapon_magic_ability.id,
    }

    response = client.put(
        f"/api/item/weapon_weapon_magic_ability/{weapon_weapon_magic_ability.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["weapon"] == weapon_weapon_magic_ability.weapon.id
    assert (
        response.data["weapon_magic_ability"]
        == weapon_weapon_magic_ability.weapon_magic_ability.id
    )


@pytest.mark.django_db
def test_weapon_weapon_magic_ability_delete_view(
    client, weapon_weapon_magic_ability_fixture
):
    weapon_weapon_magic_ability = weapon_weapon_magic_ability_fixture[0]

    response = client.delete(
        f"/api/item/weapon_weapon_magic_ability/{weapon_weapon_magic_ability.id}/"
    )

    assert response.status_code == 204
    assert not WeaponWeaponMagicAbility.objects.filter(
        id=weapon_weapon_magic_ability.id
    ).exists()


@pytest.mark.django_db
def test_armor_type_list_view(client, armor_type_fixture):
    response = client.get("/api/item/armor_type/")

    assert response.status_code == 200
    assert len(response.data) == len(armor_type_fixture)
    assert {armor["name"] for armor in response.data} == {"Light", "Medium", "Heavy"}


@pytest.mark.django_db
def test_armor_type_create_view_success(client):
    data = {"name": "Exotic"}

    response = client.post("/api/item/armor_type/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Exotic"


@pytest.mark.django_db
def test_armor_type_create_view_fail(client, armor_type_fixture):
    data = {"name": "Light"}

    response = client.post("/api/item/armor_type/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "armor type with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_armor_type_edit_view(client, armor_type_fixture):
    armor_type = armor_type_fixture[0]
    updated_data = {"name": "Updated Light"}

    response = client.put(
        f"/api/item/armor_type/{armor_type.id}/", updated_data, format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Light"


@pytest.mark.django_db
def test_armor_type_delete_view(client, armor_type_fixture):
    armor_type = armor_type_fixture[0]

    response = client.delete(f"/api/item/armor_type/{armor_type.id}/")

    assert response.status_code == 204
    assert not ArmorType.objects.filter(id=armor_type.id).exists()


@pytest.mark.django_db
def test_armor_list_view(client, armor_fixture):
    response = client.get("/api/item/armor/")

    assert response.status_code == 200
    assert len(response.data) == len(armor_fixture)
    assert {armor["name"] for armor in response.data} == {
        "Chain Shirt",
        "Breastplate",
        "Full Plate",
    }


@pytest.mark.django_db
def test_armor_create_view_success(
    client, item_category_fixture, armor_type_fixture, special_material_fixture
):
    data = {
        "name": "Studded Leather",
        "description": "Light armor made of leather with metal studs.",
        "category": item_category_fixture[0].id,
        "weight_in_lb": 15.0,
        "price_in_gp": 50.00,
        "hardness": 10,
        "hit_points": 15,
        "armor_bonus": 3,
        "max_dex_bonus": 5,
        "armor_check_penalty": -1,
        "spell_failure_chance": 15,
        "enchantment_bonus": 1,
        "armor_type": armor_type_fixture[0].id,
        "special_material": special_material_fixture[1].id,
    }

    response = client.post("/api/item/armor/", data, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Studded Leather"
    assert (
        response.data["description"] == "Light armor made of leather with metal studs."
    )


@pytest.mark.django_db
def test_armor_create_view_fail(
    client,
    armor_fixture,
    item_category_fixture,
    armor_type_fixture,
    special_material_fixture,
):
    data = {
        "name": "Chain Shirt",
        "description": "A light armor made of interlocking metal rings.",
        "category": item_category_fixture[0].id,
        "weight_in_lb": 25.0,
        "price_in_gp": 100.00,
        "hardness": 10,
        "hit_points": 20,
        "armor_bonus": 4,
        "max_dex_bonus": 4,
        "armor_check_penalty": -2,
        "spell_failure_chance": 20,
        "enchantment_bonus": 1,
        "armor_type": armor_type_fixture[0].id,
        "special_material": special_material_fixture[1].id,
    }

    response = client.post("/api/item/armor/", data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "item with this name already exists." in response.data["name"]


@pytest.mark.django_db
def test_armor_edit_view(client, armor_fixture):
    armor = armor_fixture[0]
    updated_data = {
        "name": "Updated Chain Shirt",
        "description": "Updated description for the Chain Shirt.",
        "category": armor.category.id,
        "weight_in_lb": 25.0,
        "price_in_gp": 120.00,
        "hardness": 10,
        "hit_points": 22,
        "armor_bonus": 4,
        "max_dex_bonus": 4,
        "armor_check_penalty": -2,
        "spell_failure_chance": 20,
        "enchantment_bonus": 2,
        "armor_type": armor.armor_type.id,
        "special_material": armor.special_material.id,
    }

    response = client.put(f"/api/item/armor/{armor.id}/", updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Updated Chain Shirt"
    assert response.data["description"] == "Updated description for the Chain Shirt."


@pytest.mark.django_db
def test_armor_delete_view(client, armor_fixture):
    armor = armor_fixture[0]

    response = client.delete(f"/api/item/armor/{armor.id}/")

    assert response.status_code == 204
    assert not Armor.objects.filter(id=armor.id).exists()


@pytest.mark.django_db
def test_armor_armor_magic_ability_list_view(client, armor_armor_magic_ability_fixture):
    response = client.get("/api/item/armor_armor_magic_ability/")

    assert response.status_code == 200
    assert len(response.data) == len(armor_armor_magic_ability_fixture)
    assert {aama["armor"] for aama in response.data} == {
        aama.armor.id for aama in armor_armor_magic_ability_fixture
    }
    assert {aama["armor_magic_ability"] for aama in response.data} == {
        aama.armor_magic_ability.id for aama in armor_armor_magic_ability_fixture
    }


@pytest.mark.django_db
def test_armor_armor_magic_ability_create_view_success(
    client, armor_fixture, armor_magic_ability_fixture
):
    data = {
        "armor": armor_fixture[0].id,
        "armor_magic_ability": armor_magic_ability_fixture[0].id,
    }

    response = client.post("/api/item/armor_armor_magic_ability/", data, format="json")

    assert response.status_code == 201
    assert response.data["armor"] == armor_fixture[0].id
    assert response.data["armor_magic_ability"] == armor_magic_ability_fixture[0].id


@pytest.mark.django_db
def test_armor_armor_magic_ability_create_view_fail(
    client,
    armor_armor_magic_ability_fixture,
    armor_fixture,
    armor_magic_ability_fixture,
):
    data = {
        "armor": armor_fixture[0].id,
        "armor_magic_ability": armor_magic_ability_fixture[0].id,
    }

    response = client.post("/api/item/armor_armor_magic_ability/", data, format="json")

    assert response.status_code == 400
    assert "non_field_errors" in response.data
    assert (
        "The fields armor, armor_magic_ability must make a unique set."
        in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_armor_armor_magic_ability_edit_view(client, armor_armor_magic_ability_fixture):
    armor_armor_magic_ability = armor_armor_magic_ability_fixture[0]
    updated_data = {
        "armor": armor_armor_magic_ability.armor.id,
        "armor_magic_ability": armor_armor_magic_ability.armor_magic_ability.id,
    }

    response = client.put(
        f"/api/item/armor_armor_magic_ability/{armor_armor_magic_ability.id}/",
        updated_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["armor"] == armor_armor_magic_ability.armor.id
    assert (
        response.data["armor_magic_ability"]
        == armor_armor_magic_ability.armor_magic_ability.id
    )


@pytest.mark.django_db
def test_armor_armor_magic_ability_delete_view(
    client, armor_armor_magic_ability_fixture
):
    armor_armor_magic_ability = armor_armor_magic_ability_fixture[0]

    response = client.delete(
        f"/api/item/armor_armor_magic_ability/{armor_armor_magic_ability.id}/"
    )

    assert response.status_code == 204
    assert not ArmorArmorMagicAbility.objects.filter(
        id=armor_armor_magic_ability.id
    ).exists()
