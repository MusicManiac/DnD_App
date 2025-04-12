from rest_framework.views import APIView
from rest_framework.response import Response


class APIRootView(APIView):
    """
    API root view for the D&D API.
    """

    def get(self, request):
        return Response(
            {
                "modules": {
                    "Character Module": "http://127.0.0.1:8000/api/character/",
                    "Character Class Module": "http://127.0.0.1:8000/api/character_class/",
                    "Common Module": "http://127.0.0.1:8000/api/common/",
                    "Feat Module": "http://127.0.0.1:8000/api/feat/",
                    "Item Module": "http://127.0.0.1:8000/api/item/",
                    "Race Module": "http://127.0.0.1:8000/api/race/",
                    "Skill Module": "http://127.0.0.1:8000/api/skill/",
                    "Spell Module": "http://127.0.0.1:8000/api/spell/",
                }
            }
        )
