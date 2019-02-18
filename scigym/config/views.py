from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.models import Application


@api_view(['GET'])
def app_config(request):
    application = Application.objects.get(name__iexact='github')
    config = {
        'github_client_id': settings.SOCIAL_AUTH_GITHUB_KEY,
        'github_callback_url': settings.SOCIAL_AUTH_GITHUB_CALLBACK,
        'app_client_id': application.client_id
    }
    return Response(config, status=status.HTTP_200_OK)
