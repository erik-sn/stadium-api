import logging

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from scigym.utils.errors import internal_error, GithubException
from scigym.utils.github import GithubUtils
from .models import Repository
from .serializers import RepositorySerializer


logger = logging.getLogger('django')


class RepositoryViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Repository.objects.filter(public=True)
    serializer_class = RepositorySerializer
    permission_classes = (AllowAny,)

    @action(['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def mine(self, request):
        repositories = Repository.objects.filter(owner=request.user)
        return Response(RepositorySerializer(repositories, many=True).data, status=status.HTTP_200_OK)

    @action(['POST'], detail=False, permission_classes=(IsAuthenticated,))
    def find_gym_repos(self, request, *args, **kwargs):
        try:
            logger.info(f'Searching for gym repos for user: {request.user}')
            repos = GithubUtils(request.user).create_or_refresh_gym_repos()
            return Response(RepositorySerializer(repos, many=True).data, status=status.HTTP_201_CREATED)
        except KeyError:
            return internal_error('access_token', 'no github access token found for this user')
        except GithubException:
            logger.exception('message')
            return internal_error('github', 'there was an error contacting github to request the users repositories')

    @action(['POST'], detail=True, permission_classes=(IsAuthenticated,))
    def update_gym_repo(self, request, *args, **kwargs):
        # TODO get information and update a specific repository
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
