from django.urls import path
from api.routes.merchants.search import endpoint as search_endpoint
from api.routes.merchants.ingestions import endpoint as ingest_endpoint
from api.routes.merchants.recommendations import endpoint as recommend_endpoint

urlpatterns = [
    path('merchants/', search_endpoint.search),
    path('merchants/', ingest_endpoint.injest),  
    path('merchants/<uuid:id>/recommendations', recommend_endpoint.recommend),
]
