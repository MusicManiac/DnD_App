import pytest


@pytest.mark.django_db
def test_item_category_creation(item_category_fixture):
    item_category = item_category_fixture[0]
    assert item_category.name == "Pain"
    assert item_category.description == "Yes pain is an item category."
    assert str(item_category) == "Pain"


@pytest.mark.django_db
def test_item_creation(item_fixture, item_category_fixture):
    item = item_fixture[0]
    assert item.name == "Cookie"
    assert item.description == "Omnonomnom"
    assert item.weight_in_lb == 5.5
    assert item.price_in_gp == 150.00
    assert item.hardness == 10
    assert item.hit_points == 20
    assert item.category == item_category_fixture[0]
    assert str(item) == "Cookie"


@pytest.mark.django_db
def test_special_material_creation(special_material_fixture):
    material = special_material_fixture[0]
    assert material.name == "Adamantine"
    assert material.description == "A very hard and durable material."
    assert material.link == "http://adamantine.com"
    assert str(material) == "Adamantine"


@pytest.mark.django_db
def test_weapon_magic_ability_creation(weapon_magic_ability_fixture):
    ability = weapon_magic_ability_fixture[0]
    assert ability.name == "Flaming"
    assert ability.description == "Adds fire damage to attacks."
    assert ability.caster_level_required_for_creation == 10
    assert (
        ability.other_craft_requirements
        == "Requires crafter to watch LOTR at least 5 times"
    )
    assert ability.cost_increase_in_bonus == 1
    assert str(ability) == "Flaming"


@pytest.mark.django_db
def test_weapon_magic_ability_feat_creation(
    weapon_magic_ability_feat_fixture, weapon_magic_ability_fixture, feat_fixture
):
    weapon_magic_ability_feat = weapon_magic_ability_feat_fixture[0]
    assert (
        weapon_magic_ability_feat.weapon_magic_ability
        == weapon_magic_ability_fixture[0]
    )
    assert weapon_magic_ability_feat.feat == feat_fixture[0]


@pytest.mark.django_db
def test_weapon_magic_ability_spell_creation(
    weapon_magic_ability_spell_fixture, weapon_magic_ability_fixture, spell_fixture
):
    weapon_magic_ability_spell = weapon_magic_ability_spell_fixture[0]
    assert (
        weapon_magic_ability_spell.weapon_magic_ability
        == weapon_magic_ability_fixture[0]
    )
    assert weapon_magic_ability_spell.spell == spell_fixture[0]


@pytest.mark.django_db
def test_armor_magic_ability_creation(
    armor_magic_ability_fixture, magic_aura_strength_fixture, magic_school_fixture
):
    ability = armor_magic_ability_fixture[0]
    assert ability.name == "Fortification"
    assert ability.description == "Provides a chance to negate critical hits."
    assert ability.caster_level_required_for_creation == 13
    assert ability.cost_increase_in_bonus == 3
    assert ability.magic_aura_strength == magic_aura_strength_fixture[2]
    assert ability.magic_aura_type == magic_school_fixture[1]
    assert str(ability) == "Fortification"


@pytest.mark.django_db
def test_armor_magic_ability_feat_creation(
    armor_magic_ability_feat_fixture, armor_magic_ability_fixture, feat_fixture
):
    armor_magic_ability_feat = armor_magic_ability_feat_fixture[0]
    assert (
        armor_magic_ability_feat.armor_magic_ability == armor_magic_ability_fixture[0]
    )
    assert armor_magic_ability_feat.feat == feat_fixture[0]


@pytest.mark.django_db
def test_armor_magic_ability_spell_creation(
    armor_magic_ability_spell_fixture, armor_magic_ability_fixture, spell_fixture
):
    armor_magic_ability_spell = armor_magic_ability_spell_fixture[0]
    assert (
        armor_magic_ability_spell.armor_magic_ability == armor_magic_ability_fixture[0]
    )
    assert armor_magic_ability_spell.spell == spell_fixture[0]


@pytest.mark.django_db
def test_weapon_category_creation(weapon_category_fixture):
    category = weapon_category_fixture[0]
    assert category.name == "Simple"
    assert category.description == "Basic weapons that require minimal training."
    assert str(category) == "Simple"


@pytest.mark.django_db
def test_weapon_damage_type_creation(weapon_damage_type_fixture):
    damage_type = weapon_damage_type_fixture[0]
    assert damage_type.name == "Bludgeoning"
    assert damage_type.description == "Smashing"
    assert str(damage_type) == "Bludgeoning"


@pytest.mark.django_db
def test_weapon_creation(
    weapon_fixture,
    weapon_damage_type_fixture,
    special_material_fixture,
    item_category_fixture,
):
    weapon = weapon_fixture[0]
    assert weapon.name == "Longsword full properties"
    assert weapon.description == "A versatile sword."
    assert weapon.category == item_category_fixture[0]
    assert weapon.weight_in_lb == 5.5
    assert weapon.price_in_gp == 150.00
    assert weapon.hardness == 10
    assert weapon.hit_points == 20
    assert weapon.damage == "1d8"
    assert weapon.crit_multiplier == 2
    assert weapon.crit_range == "19-20"
    assert weapon.range_increment_in_ft == 20
    assert weapon.is_masterwork is True
    assert weapon.enchantment_bonus == 1
    assert weapon.special_material == special_material_fixture[0]
    assert weapon.weapon_damage_type == weapon_damage_type_fixture[0]
    assert str(weapon) == "Longsword full properties"


@pytest.mark.django_db
def test_weapon_weapon_category_creation(
    weapon_weapon_category_fixture, weapon_fixture, weapon_category_fixture
):
    weapon_weapon_category = weapon_weapon_category_fixture[0]
    assert weapon_weapon_category.weapon == weapon_fixture[0]
    assert weapon_weapon_category.weapon_category == weapon_category_fixture[0]


@pytest.mark.django_db
def test_weapon_weapon_damage_type_creation(
    weapon_weapon_damage_type_fixture, weapon_fixture, weapon_damage_type_fixture
):
    weapon_weapon_damage_type = weapon_weapon_damage_type_fixture[0]
    assert weapon_weapon_damage_type.weapon == weapon_fixture[0]
    assert weapon_weapon_damage_type.weapon_damage_type == weapon_damage_type_fixture[0]


@pytest.mark.django_db
def test_weapon_weapon_magic_ability_creation(
    weapon_weapon_magic_ability_fixture, weapon_fixture, weapon_magic_ability_fixture
):
    weapon_weapon_magic_ability = weapon_weapon_magic_ability_fixture[0]
    assert weapon_weapon_magic_ability.weapon == weapon_fixture[0]
    assert (
        weapon_weapon_magic_ability.weapon_magic_ability
        == weapon_magic_ability_fixture[0]
    )


@pytest.mark.django_db
def test_armor_type_creation(armor_type_fixture):
    armor_type = armor_type_fixture[0]
    assert armor_type.name == "Light"
    assert str(armor_type) == "Light"


@pytest.mark.django_db
def test_armor_creation(
    armor_fixture, item_category_fixture, armor_type_fixture, special_material_fixture
):
    armor = armor_fixture[0]
    assert armor.name == "Chain Shirt"
    assert armor.description == "A light armor made of interlocking metal rings."
    assert armor.category == item_category_fixture[0]
    assert armor.weight_in_lb == 25.0
    assert armor.price_in_gp == 100.00
    assert armor.hardness == 10
    assert armor.hit_points == 20
    assert armor.armor_bonus == 4
    assert armor.max_dex_bonus == 4
    assert armor.armor_check_penalty == -2
    assert armor.spell_failure_chance == 20
    assert armor.enchantment_bonus == 1
    assert armor.armor_type == armor_type_fixture[0]
    assert armor.special_material == special_material_fixture[1]
    assert str(armor) == "Chain Shirt"


@pytest.mark.django_db
def test_armor_armor_magic_ability_creation(
    armor_armor_magic_ability_fixture, armor_fixture, armor_magic_ability_fixture
):
    armor_armor_magic_ability = armor_armor_magic_ability_fixture[0]
    assert armor_armor_magic_ability.armor == armor_fixture[0]
    assert (
        armor_armor_magic_ability.armor_magic_ability == armor_magic_ability_fixture[0]
    )
