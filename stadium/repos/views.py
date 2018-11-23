import logging

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from stadium.utils.errors import internal_error, GithubException
from stadium.utils.github import GithubUtils
from .models import Repo
from .serializers import RepoSerializer


logger = logging.getLogger('django')


class RepoViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Repo.objects.filter(private=False)
    serializer_class = RepoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(['POST'], detail=False)
    def find_gym_repos(self, request, *args, **kwargs):
        try:
            logger.info(f'Searching for gym repos for user: {request.user}')
            repos = GithubUtils(request.user).create_or_refresh_gym_repos()
            return Response(RepoSerializer(repos, many=True).data, status=status.HTTP_201_CREATED)
        except KeyError:
            return internal_error('access_token', 'no github access token found for this user')
        except GithubException:
            logger.exception('message')
            return internal_error('github', 'there was an error contacting github to request the users repositories')

    @action(['POST'], detail=True)
    def update_gym_repo(self, request, *args, **kwargs):
        # TODO get information and update a specific repository
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)



