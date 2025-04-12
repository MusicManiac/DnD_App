from character.models import (
    Inventory,
    InventoryItem,
    Character,
    CharacterAbilityScore,
    CharacterCharacterClass,
    CharacterFeat,
    CharacterLanguage,
    CharacterInventory,
    CharacterSkill,
)
from character.serializers import (
    InventorySerializer,
    InventoryItemSerializer,
    CharacterSerializer,
    CharacterAbilityScoreSerializer,
    CharacterCharacterClassSerializer,
    CharacterFeatSerializer,
    CharacterLanguageSerializer,
    CharacterInventorySerializer,
    CharacterSkillSerializer,
)
from utils.views import CustomModelViewSet


class InventoryViewSet(CustomModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryItemViewSet(CustomModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    custom_view_name = "(Inventory - Item) List"


class CharacterViewSet(CustomModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class CharacterAbilityScoreViewSet(CustomModelViewSet):
    queryset = CharacterAbilityScore.objects.all()
    serializer_class = CharacterAbilityScoreSerializer
    custom_view_name = "(Character - Ability Score) List"


class CharacterCharacterClassViewSet(CustomModelViewSet):
    queryset = CharacterCharacterClass.objects.all()
    serializer_class = CharacterCharacterClassSerializer
    custom_view_name = "(Character - Character Class) List"


class CharacterFeatViewSet(CustomModelViewSet):
    queryset = CharacterFeat.objects.all()
    serializer_class = CharacterFeatSerializer
    custom_view_name = "(Character - Feat) List"


class CharacterLanguageViewSet(CustomModelViewSet):
    queryset = CharacterLanguage.objects.all()
    serializer_class = CharacterLanguageSerializer
    custom_view_name = "(Character - Language) List"


class CharacterInventoryViewSet(CustomModelViewSet):
    queryset = CharacterInventory.objects.all()
    serializer_class = CharacterInventorySerializer
    custom_view_name = "(Character - Inventory) List"


class CharacterSkillViewSet(CustomModelViewSet):
    queryset = CharacterSkill.objects.all()
    serializer_class = CharacterSkillSerializer
    custom_view_name = "(Character - Skill) List"
