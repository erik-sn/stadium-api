import logging

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from scigym.utils.errors import internal_error, GithubException
from scigym.utils.github import GithubApiClient
from .models import Contributor
from .serializers import ContributorSerializer
from .permissions import IsAdminOrReadOnly


logger = logging.getLogger('django')


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(['POST'], detail=False)
    def find_contributors(self, request):
        try:
            contributors = GithubApiClient(None).create_or_refresh_contributors()
            return Response(ContributorSerializer(contributors, many=True).data, status=status.HTTP_201_CREATED)
        except GithubException:
            logger.exception('message')
            return internal_error('github', 'there was an error contacting github to request the users repositories')
