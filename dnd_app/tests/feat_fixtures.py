import pytest

from feat.models import (
    TypeOfFeat,
    Feat,
    FeatTypeOfFeat,
    FeatAbilityPrerequisite,
    FeatFeatPrerequisite,
    FeatSkillPrerequisite,
)


@pytest.fixture()
def type_of_feat_fixture():
    return TypeOfFeat.objects.bulk_create(
        [
            TypeOfFeat(name="General", description="Well it's general"),
            TypeOfFeat(name="Ultra-giga-specialized", description="Huh?"),
        ]
    )


@pytest.fixture()
def feat_fixture():
    return Feat.objects.bulk_create(
        [
            Feat(
                name="Feat 1",
                benefit="Benefit 1",
                normal="Normal 1",
                special="Special 1",
                other_prerequisites="Other prerequisites 1",
                link="https://netlix.com",
            ),
            Feat(name="Feat 2", benefit="Benefit 2"),
            Feat(name="Feat 3", benefit="Benefit 3"),
            Feat(name="Feat 4", benefit="Benefit 4"),
        ]
    )


@pytest.fixture()
def feat_type_of_feat_fixture(feat_fixture, type_of_feat_fixture):
    return FeatTypeOfFeat.objects.bulk_create(
        [
            FeatTypeOfFeat(feat=feat_fixture[0], type_of_feat=type_of_feat_fixture[0]),
            FeatTypeOfFeat(feat=feat_fixture[1], type_of_feat=type_of_feat_fixture[0]),
            FeatTypeOfFeat(feat=feat_fixture[2], type_of_feat=type_of_feat_fixture[1]),
            FeatTypeOfFeat(feat=feat_fixture[3], type_of_feat=type_of_feat_fixture[1]),
        ]
    )


@pytest.fixture()
def feat_ability_prerequisite_fixture(feat_fixture, ability_fixture):
    return FeatAbilityPrerequisite.objects.bulk_create(
        [
            FeatAbilityPrerequisite(
                feat=feat_fixture[0],
                ability=ability_fixture[0],
                required_ability_value=15,
            ),
            FeatAbilityPrerequisite(
                feat=feat_fixture[1],
                ability=ability_fixture[0],
                required_ability_value=12,
            ),
            FeatAbilityPrerequisite(
                feat=feat_fixture[2],
                ability=ability_fixture[1],
                required_ability_value=10,
            ),
            FeatAbilityPrerequisite(
                feat=feat_fixture[3],
                ability=ability_fixture[2],
                required_ability_value=8,
            ),
        ]
    )


@pytest.fixture()
def feat_feat_prerequisite_fixture(feat_fixture):
    return FeatFeatPrerequisite.objects.bulk_create(
        [
            FeatFeatPrerequisite(
                prerequisite_for_feat=feat_fixture[0],
                prerequisite=feat_fixture[1],
            ),
            FeatFeatPrerequisite(
                prerequisite_for_feat=feat_fixture[2],
                prerequisite=feat_fixture[1],
            ),
        ]
    )


@pytest.fixture()
def feat_skill_prerequisite_fixture(feat_fixture, skill_fixture):
    return FeatSkillPrerequisite.objects.bulk_create(
        [
            FeatSkillPrerequisite(
                feat=feat_fixture[0], skill=skill_fixture[0], required_ranks=4
            ),
            FeatSkillPrerequisite(
                feat=feat_fixture[1], skill=skill_fixture[1], required_ranks=2
            ),
            FeatSkillPrerequisite(
                feat=feat_fixture[2], skill=skill_fixture[1], required_ranks=6
            ),
        ]
    )
