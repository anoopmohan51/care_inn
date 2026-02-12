from rest_framework.permissions import BasePermission
from core_api.models.external_api_key import ExternalApiKey
import os

class HasValidApiKey(BasePermission):

    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return False
        return ExternalApiKey.objects.filter(key=api_key,is_active=True).exists()


class HasValidApiKeyForPatientApp(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        print(api_key)
        api_key_env = os.environ.get('CAREINN_API_KEY')
        print(api_key_env)
        if not api_key:
            print("api_key is not present1")
            return False
        if api_key == api_key_env:
            print("api_key is present")
            return True
        print("api_key is not present2")
        return False