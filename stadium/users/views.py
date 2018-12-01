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
from django.shortcuts import get_object_or_404

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

    @action(methods=['GET'], detail=False)
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


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
            convert_response = self._convert_github_token_to_app_token(github_access_token)
            if 'error' in convert_response.json():
                return Response(convert_response.json(), status=status.HTTP_400_BAD_REQUEST)

            user_access_token = convert_response.json()['accessToken']
            user = AccessToken.objects.get(token=user_access_token).user
            user_data = UserSerializer(user).data

            return Response({**convert_response.json(), **user_data}, status=convert_response.status_code)
        except GithubException as exception:
            logger.exception('message')
            raise exception

    @action(methods=['POST'], detail=True)
    def refresh_token(self, request, pk=None):
        endpoint = settings.API_HOST + reverse('token')
        application = Application.objects.get(name__iexact='github')
        response = requests.post(endpoint, params={
            'grant_type': 'refresh_token',
            'client_id': application.client_id,
            'client_secret': application.client_secret,
            'refresh_token': pk,
        })
        logger.info(response.content)
        return Response(response.json(), status=response.status_code)

