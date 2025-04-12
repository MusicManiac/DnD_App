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
    WeaponDamageType,
    WeaponCategory,
    Weapon,
    WeaponWeaponCategory,
    WeaponWeaponDamageType,
    WeaponWeaponMagicAbility,
    ArmorType,
    Armor,
    ArmorArmorMagicAbility,
)


@pytest.fixture()
def item_category_fixture():
    return ItemCategory.objects.bulk_create(
        [
            ItemCategory(
                name="Pain",
                description="Yes pain is an item category.",
            ),
            ItemCategory(
                name="Suffering",
                description="Maybe this too xdd",
            ),
            ItemCategory(
                name="TestCategory",
            ),
        ]
    )


@pytest.fixture()
def item_fixture(item_category_fixture):
    return Item.objects.bulk_create(
        [
            Item(
                name="Cookie",
                description="Omnonomnom",
                weight_in_lb=5.5,
                price_in_gp=150.00,
                hardness=10,
                hit_points=20,
                category=item_category_fixture[0],
            ),
            Item(
                name="Keyboard",
                description="What keyboard is doing in dnd?",
                weight_in_lb=8.0,
                price_in_gp=200.00,
                hardness=15,
                hit_points=25,
                category=item_category_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def special_material_fixture():
    return SpecialMaterial.objects.bulk_create(
        [
            SpecialMaterial(
                name="Adamantine",
                description="A very hard and durable material.",
                link="http://adamantine.com",
            ),
            SpecialMaterial(
                name="Mithral",
            ),
        ]
    )


@pytest.fixture()
def weapon_magic_ability_fixture(magic_aura_strength_fixture, magic_school_fixture):
    return WeaponMagicAbility.objects.bulk_create(
        [
            WeaponMagicAbility(
                name="Flaming",
                description="Adds fire damage to attacks.",
                caster_level_required_for_creation=10,
                other_craft_requirements="Requires crafter to watch LOTR at least 5 times",
                cost_increase_in_bonus=1,
                magic_aura_strength=magic_aura_strength_fixture[0],
                magic_aura_type=magic_school_fixture[0],
            ),
            WeaponMagicAbility(
                name="Frost",
                description="Adds cold damage to attacks.",
                caster_level_required_for_creation=10,
                cost_increase_in_bonus=1,
                magic_aura_strength=magic_aura_strength_fixture[1],
                magic_aura_type=magic_school_fixture[1],
            ),
            WeaponMagicAbility(
                name="Frost222",
                description="Adds 222 cold damage to attacks.",
                caster_level_required_for_creation=10,
                cost_increase_in_bonus=2,
                magic_aura_strength=magic_aura_strength_fixture[2],
                magic_aura_type=magic_school_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def weapon_magic_ability_feat_fixture(weapon_magic_ability_fixture, feat_fixture):
    return WeaponMagicAbilityFeat.objects.bulk_create(
        [
            WeaponMagicAbilityFeat(
                weapon_magic_ability=weapon_magic_ability_fixture[0],
                feat=feat_fixture[0],
            ),
            WeaponMagicAbilityFeat(
                weapon_magic_ability=weapon_magic_ability_fixture[1],
                feat=feat_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def weapon_magic_ability_spell_fixture(weapon_magic_ability_fixture, spell_fixture):
    return WeaponMagicAbilitySpell.objects.bulk_create(
        [
            WeaponMagicAbilitySpell(
                weapon_magic_ability=weapon_magic_ability_fixture[0],
                spell=spell_fixture[0],
            ),
            WeaponMagicAbilitySpell(
                weapon_magic_ability=weapon_magic_ability_fixture[1],
                spell=spell_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def armor_magic_ability_fixture(magic_aura_strength_fixture, magic_school_fixture):
    return ArmorMagicAbility.objects.bulk_create(
        [
            ArmorMagicAbility(
                name="Fortification",
                description="Provides a chance to negate critical hits.",
                caster_level_required_for_creation=13,
                cost_increase_in_bonus=3,
                magic_aura_strength=magic_aura_strength_fixture[2],
                magic_aura_type=magic_school_fixture[1],
            ),
            ArmorMagicAbility(
                name="Shadow",
                description="Improves stealth capabilities.",
                caster_level_required_for_creation=5,
                cost_increase_in_bonus=1,
                magic_aura_strength=magic_aura_strength_fixture[2],
                magic_aura_type=magic_school_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def armor_magic_ability_feat_fixture(armor_magic_ability_fixture, feat_fixture):
    return ArmorMagicAbilityFeat.objects.bulk_create(
        [
            ArmorMagicAbilityFeat(
                armor_magic_ability=armor_magic_ability_fixture[0],
                feat=feat_fixture[0],
            ),
            ArmorMagicAbilityFeat(
                armor_magic_ability=armor_magic_ability_fixture[1],
                feat=feat_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def armor_magic_ability_spell_fixture(armor_magic_ability_fixture, spell_fixture):
    return ArmorMagicAbilitySpell.objects.bulk_create(
        [
            ArmorMagicAbilitySpell(
                armor_magic_ability=armor_magic_ability_fixture[0],
                spell=spell_fixture[0],
            ),
            ArmorMagicAbilitySpell(
                armor_magic_ability=armor_magic_ability_fixture[1],
                spell=spell_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def weapon_category_fixture():
    return WeaponCategory.objects.bulk_create(
        [
            WeaponCategory(
                name="Simple",
                description="Basic weapons that require minimal training.",
            ),
            WeaponCategory(
                name="Martial",
                description="Weapons requiring more training to use effectively.",
            ),
            WeaponCategory(
                name="Exotic",
                description="Specialized weapons requiring specific training.",
            ),
        ]
    )


@pytest.fixture()
def weapon_damage_type_fixture():
    return WeaponDamageType.objects.bulk_create(
        [
            WeaponDamageType(
                name="Bludgeoning",
                description="Smashing",
            ),
            WeaponDamageType(
                name="Piercing",
                description="Poking",
            ),
            WeaponDamageType(
                name="Slashing",
                description="Slicing",
            ),
        ]
    )


@pytest.fixture()
def weapon_fixture(
    weapon_damage_type_fixture, special_material_fixture, item_category_fixture
):
    return [
        Weapon.objects.create(
            name="Longsword full properties",
            description="A versatile sword.",
            category=item_category_fixture[0],
            weight_in_lb=5.5,
            price_in_gp=150.00,
            hardness=10,
            hit_points=20,
            damage="1d8",
            crit_multiplier=2,
            crit_range="19-20",
            range_increment_in_ft=20,
            is_masterwork=True,
            enchantment_bonus=1,
            special_material=special_material_fixture[0],
            weapon_damage_type=weapon_damage_type_fixture[0],
        ),
        Weapon.objects.create(
            name="Longsword",
            description="A versatile sword.",
            category=item_category_fixture[0],
            weight_in_lb=5.5,
            price_in_gp=150.00,
            hardness=10,
            hit_points=20,
            weapon_damage_type=weapon_damage_type_fixture[1],
        ),
        Weapon.objects.create(
            name="warhammer",
            description="A versatile sword.",
            category=item_category_fixture[0],
            weight_in_lb=5.5,
            price_in_gp=150.00,
            hardness=10,
            hit_points=20,
            weapon_damage_type=weapon_damage_type_fixture[2],
        ),
    ]


@pytest.fixture()
def weapon_weapon_category_fixture(weapon_fixture, weapon_category_fixture):
    return WeaponWeaponCategory.objects.bulk_create(
        [
            WeaponWeaponCategory(
                weapon=weapon_fixture[0],
                weapon_category=weapon_category_fixture[0],
            ),
            WeaponWeaponCategory(
                weapon=weapon_fixture[1],
                weapon_category=weapon_category_fixture[1],
            ),
            WeaponWeaponCategory(
                weapon=weapon_fixture[2],
                weapon_category=weapon_category_fixture[2],
            ),
        ]
    )


@pytest.fixture()
def weapon_weapon_damage_type_fixture(weapon_fixture, weapon_damage_type_fixture):
    return WeaponWeaponDamageType.objects.bulk_create(
        [
            WeaponWeaponDamageType(
                weapon=weapon_fixture[0],
                weapon_damage_type=weapon_damage_type_fixture[0],
            ),
            WeaponWeaponDamageType(
                weapon=weapon_fixture[1],
                weapon_damage_type=weapon_damage_type_fixture[1],
            ),
            WeaponWeaponDamageType(
                weapon=weapon_fixture[2],
                weapon_damage_type=weapon_damage_type_fixture[2],
            ),
        ]
    )


@pytest.fixture()
def weapon_weapon_magic_ability_fixture(weapon_fixture, weapon_magic_ability_fixture):
    return WeaponWeaponMagicAbility.objects.bulk_create(
        [
            WeaponWeaponMagicAbility(
                weapon=weapon_fixture[0],
                weapon_magic_ability=weapon_magic_ability_fixture[0],
            ),
            WeaponWeaponMagicAbility(
                weapon=weapon_fixture[1],
                weapon_magic_ability=weapon_magic_ability_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def armor_type_fixture():
    return ArmorType.objects.bulk_create(
        [
            ArmorType(name="Light"),
            ArmorType(name="Medium"),
            ArmorType(name="Heavy"),
        ]
    )


@pytest.fixture()
def armor_fixture(item_category_fixture, armor_type_fixture, special_material_fixture):
    return [
        Armor.objects.create(
            name="Chain Shirt",
            description="A light armor made of interlocking metal rings.",
            category=item_category_fixture[0],
            weight_in_lb=25.0,
            price_in_gp=100.00,
            hardness=10,
            hit_points=20,
            armor_bonus=4,
            max_dex_bonus=4,
            armor_check_penalty=-2,
            spell_failure_chance=20,
            enchantment_bonus=1,
            armor_type=armor_type_fixture[0],
            special_material=special_material_fixture[1],
        ),
        Armor.objects.create(
            name="Breastplate",
            description="A medium armor offering good protection.",
            category=item_category_fixture[1],
            weight_in_lb=30.0,
            price_in_gp=200.00,
            hardness=15,
            hit_points=30,
        ),
        Armor.objects.create(
            name="Full Plate",
            description="A heavy armor providing excellent protection.",
            category=item_category_fixture[0],
            weight_in_lb=50.0,
            price_in_gp=1500.00,
            hardness=20,
            hit_points=40,
        ),
    ]


@pytest.fixture()
def armor_armor_magic_ability_fixture(armor_fixture, armor_magic_ability_fixture):
    return ArmorArmorMagicAbility.objects.bulk_create(
        [
            ArmorArmorMagicAbility(
                armor=armor_fixture[0],
                armor_magic_ability=armor_magic_ability_fixture[0],
            ),
            ArmorArmorMagicAbility(
                armor=armor_fixture[1],
                armor_magic_ability=armor_magic_ability_fixture[1],
            ),
        ]
    )
