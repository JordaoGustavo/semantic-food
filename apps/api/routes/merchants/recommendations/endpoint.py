from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.routes.merchants.llm_service import LLMService
from api.routes.merchants.repository import MongoRagSearchRepository


@api_view(['GET'])
def recommend(request, id=None):
    merchants_repository = MongoRagSearchRepository.create()
    merchant = merchants_repository.get(str(id))

    if not merchant:
        return Response({"message": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)

    merchants = list(merchants_repository.semantic_search(merchant['content_description_embedding']))
    return Response(merchants)