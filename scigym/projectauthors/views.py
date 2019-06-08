import logging

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response

from scigym.config.permissions import IsAdminOrReadOnly
from scigym.utils.errors import internal_error, GithubException
from scigym.utils.github import GithubApiClient
from .models import ProjectAuthor
from .serializers import ProjectAuthorSerializer

logger = logging.getLogger('django')

class ProjectAuthorViewSet(viewsets.ModelViewSet):
    queryset = ProjectAuthor.objects.all()
    serializer_class = ProjectAuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)
