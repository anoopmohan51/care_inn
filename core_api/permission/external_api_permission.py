from rest_framework.permissions import BasePermission
from core_api.models.external_api_key import ExternalApiKey

class HasValidApiKey(BasePermission):

    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return False
        return ExternalApiKey.objects.filter(key=api_key,is_active=True).exists()