from django.urls import path, include
from api.routes.healthcheck import endpoint as healthcheck_endpoint

urlpatterns = [
    path('health/', healthcheck_endpoint.check_health), 
    path('', include('api.routes.merchants.urls')) 
]
