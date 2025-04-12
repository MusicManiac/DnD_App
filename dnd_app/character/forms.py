from django import forms

from character_class.models import CharacterClass
from common.models import Ability, Language
from feat.models import Feat
from .models import (
    Character,
    CharacterSkill,
    CharacterLanguage,
    CharacterCharacterClass,
)


class CharacterCharacterClassForm(forms.ModelForm):
    def save(self, commit=True):
        character_character_class = super().save(commit=commit)
        self.add_skills_to_character(character_character_class)
        return character_character_class

    def add_skills_to_character(self, character_character_class):
        """
        Adds the skills from the character's class to the character.
        """
        # Get the character class linked to this character
        character_class = character_character_class.character_class

        for class_skill in character_class.class_skills.all():
            CharacterSkill.objects.get_or_create(
                character=character_character_class.character, skill=class_skill
            )

    class Meta:
        model = CharacterCharacterClass
        fields = ["character", "character_class", "level"]


class CharacterForm(forms.ModelForm):
    def create_m2m_languages(self, character):
        """
        Creates the many-to-many relationship between character and automatic languages from race
        """
        race_languages = character.race.racelanguage_set.filter(is_automatic=True)
        for race_language in race_languages:
            CharacterLanguage.objects.get_or_create(
                character=character, language=race_language.language, is_automatic=True
            )

    def save(self, commit=True):
        character = super().save(commit=True)
        if commit:
            character.save()
        return character

    def save_m2m(self):
        self.create_m2m_languages(self.instance)
        return self.instance

    class Meta:
        model = Character
        fields = "__all__"
