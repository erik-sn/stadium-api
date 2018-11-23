import logging

import requests
from oauth2_provider.admin import AccessToken
from oauth2_provider.models import Application
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings

from stadium.utils.errors import GithubException
from stadium.utils.github import GithubApiClient
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer

logger = logging.getLogger('django')


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def _convert_github_token_to_app_token(access_token):
        endpoint = settings.API_HOST + reverse('convert_token')
        application = Application.objects.get(name__iexact='github')
        return requests.post(endpoint, params={
            'grant_type': 'convert_token',
            'client_id': application.client_id,
            'client_secret': application.client_secret,
            'backend': 'github',
            'token': access_token,
        })

    @action(methods=['POST'], detail=True)
    def github_oauth(self, request, pk=None):
        try:
            client = GithubApiClient(user=None)
            github_response = client.get_access_token(pk)
            if 'error' in github_response.json():
                return Response(github_response.json(), status=status.HTTP_400_BAD_REQUEST)

            github_access_token = github_response.json()['access_token']
            response = self._convert_github_token_to_app_token(github_access_token)

            user_access_token = response.json()['access_token']
            user = AccessToken.objects.get(token=user_access_token).user

            user_data = UserSerializer(user).data

            return Response({**response.json(), **user_data}, status=response.status_code)
        except GithubException as exception:
            logger.exception('message')
            raise exception




