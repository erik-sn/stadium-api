from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def app_config(request):
    config = {
        'github_client_id': settings.SOCIAL_AUTH_GITHUB_KEY
    }
    return Response(config, status=status.HTTP_200_OK)
