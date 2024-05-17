from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from api.routes.merchants.llm_service import LLMService
from api.routes.merchants.repository import MongoRagSearchRepository

@api_view(['GET'])
def search(request):
    name_value = request.query_params.get('name', None)
    repository = MongoRagSearchRepository.create()
    if name_value is None:
        results = {
            "text_search": list(repository.get_random()),
            "recommendation": []
        }
        return Response(results)
    
    service = LLMService()

    query_embedding = service.generate_embedding(name_value)
    query = {
        "embedding": query_embedding,
        "text_search": name_value
    }
    results = repository.hybrid_search(query)
    return Response(results) 