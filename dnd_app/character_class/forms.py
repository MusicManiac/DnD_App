from django import forms

from common.models import Die
from .models import CharacterClass


class CharacterClassForm(forms.ModelForm):
    hit_die = forms.ModelChoiceField(
        queryset=Die.objects.filter(sides__in=[4, 6, 8, 10, 12]),
        empty_label="Choose a hit die",
        required=True,
    )

    class Meta:
        model = CharacterClass
        fields = "__all__"
