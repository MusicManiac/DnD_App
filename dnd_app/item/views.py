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
from item.serializers import (
    ItemCategorySerializer,
    ItemSerializer,
    SpecialMaterialSerializer,
    WeaponMagicAbilitySerializer,
    WeaponMagicAbilityFeatSerializer,
    WeaponMagicAbilitySpellSerializer,
    ArmorMagicAbilitySerializer,
    ArmorMagicAbilityFeatSerializer,
    ArmorMagicAbilitySpellSerializer,
    WeaponCategorySerializer,
    WeaponDamageTypeSerializer,
    WeaponSerializer,
    WeaponWeaponCategorySerializer,
    WeaponWeaponDamageTypeSerializer,
    WeaponWeaponMagicAbilitySerializer,
    ArmorTypeSerializer,
    ArmorSerializer,
    ArmorArmorMagicAbilitySerializer,
)
from utils.views import CustomModelViewSet


class ItemCategoryViewSet(CustomModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer


class ItemViewSet(CustomModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class SpecialMaterialViewSet(CustomModelViewSet):
    queryset = SpecialMaterial.objects.all()
    serializer_class = SpecialMaterialSerializer


class WeaponMagicAbilityViewSet(CustomModelViewSet):
    queryset = WeaponMagicAbility.objects.all()
    serializer_class = WeaponMagicAbilitySerializer


class WeaponMagicAbilityFeatViewSet(CustomModelViewSet):
    queryset = WeaponMagicAbilityFeat.objects.all()
    serializer_class = WeaponMagicAbilityFeatSerializer
    custom_view_name = "(Weapon Magic Ability - Feat) List"


class WeaponMagicAbilitySpellViewSet(CustomModelViewSet):
    queryset = WeaponMagicAbilitySpell.objects.all()
    serializer_class = WeaponMagicAbilitySpellSerializer
    custom_view_name = "(Weapon Magic Ability - Spell) List"


class ArmorMagicAbilityViewSet(CustomModelViewSet):
    queryset = ArmorMagicAbility.objects.all()
    serializer_class = ArmorMagicAbilitySerializer


class ArmorMagicAbilityFeatViewSet(CustomModelViewSet):
    queryset = ArmorMagicAbilityFeat.objects.all()
    serializer_class = ArmorMagicAbilityFeatSerializer
    custom_view_name = "(Armor Magic Ability - Feat) List"


class ArmorMagicAbilitySpellViewSet(CustomModelViewSet):
    queryset = ArmorMagicAbilitySpell.objects.all()
    serializer_class = ArmorMagicAbilitySpellSerializer
    custom_view_name = "(Armor Magic Ability - Spell) List"


class WeaponCategoryViewSet(CustomModelViewSet):
    queryset = WeaponCategory.objects.all()
    serializer_class = WeaponCategorySerializer
    custom_view_name = "(Weapon - Category) List"


class WeaponDamageTypeViewSet(CustomModelViewSet):
    queryset = WeaponDamageType.objects.all()
    serializer_class = WeaponDamageTypeSerializer
    custom_view_name = "(Weapon - Damage Type) List"


class WeaponViewSet(CustomModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer


class WeaponWeaponCategoryViewSet(CustomModelViewSet):
    queryset = WeaponWeaponCategory.objects.all()
    serializer_class = WeaponWeaponCategorySerializer
    custom_view_name = "(Weapon - Weapon Category) List"


class WeaponWeaponDamageTypeViewSet(CustomModelViewSet):
    queryset = WeaponWeaponDamageType.objects.all()
    serializer_class = WeaponWeaponDamageTypeSerializer
    custom_view_name = "(Weapon - Weapon Damage Type) List"


class WeaponWeaponMagicAbilityViewSet(CustomModelViewSet):
    queryset = WeaponWeaponMagicAbility.objects.all()
    serializer_class = WeaponWeaponMagicAbilitySerializer
    custom_view_name = "(Weapon - Weapon Magic Ability) List"


class ArmorTypeViewSet(CustomModelViewSet):
    queryset = ArmorType.objects.all()
    serializer_class = ArmorTypeSerializer


class ArmorViewSet(CustomModelViewSet):
    queryset = Armor.objects.all()
    serializer_class = ArmorSerializer


class ArmorArmorMagicAbilityViewSet(CustomModelViewSet):
    queryset = ArmorArmorMagicAbility.objects.all()
    serializer_class = ArmorArmorMagicAbilitySerializer
    custom_view_name = "(Armor - Armor Magic Ability) List"
