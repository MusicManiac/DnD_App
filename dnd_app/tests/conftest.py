import pytest
from rest_framework.test import APIClient
from .common_fixtures import *
from .skill_fixtures import *
from .feat_fixtures import *
from .race_fixtures import *
from .character_class_fixtures import *
from .spell_fixtures import *
from .item_fixtures import *


@pytest.fixture()
def client():
    return APIClient()
