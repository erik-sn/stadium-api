import logging
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from rest_framework import viewsets, status

from scigym.repositories.models import Repository
from .models import Environment
from .serializers import (
    EnvironmentSerializer,
    EnvironmentWriteSerializer
)
from .permissions import IsOwnerOrReadOnly

logger = logging.getLogger('django')

WRITE_VERBS = ['POST', 'PUT']


class EnvironmentViewSet(viewsets.ModelViewSet):
    """
    View to create environments
    """
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        return EnvironmentWriteSerializer if self.request.method in WRITE_VERBS else self.serializer_class

    def create(self, request):
        env = Environment.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            repository=Repository.objects.get(id=request.data['repository']),
            tags=request.data['tags']
        )
        serializer = EnvironmentWriteSerializer(env)
        return Response(serializer.data, status=201)

    def delete(self, request, pk):
        env =  get_object_or_404(pk)
        env.delete()
        return(Response(status=status.HTTP_204_NO_CONTENT))

    @action(['GET'], detail=False)
    def filter(self, request):

        from django.db.models import Q

        search_terms = request.GET.get('search', '').split(',')
        if len(search_terms) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        query = Q(name__isnull=False)  # initialize the query with a condition we always know is true
        search_query = query
        for i, term in enumerate(search_terms):
            if not i:
                search_query = Q(name__icontains=term) | Q(tags__icontains=term)
            else:
                search_query |= Q(name__icontains=term)
                search_query |= Q(tags__icontains=term)
        query &= search_query
        logger.debug(query)

        environments = Environment.objects.filter(query).select_related('repository')

        serializer = EnvironmentSerializer(environments, many=True)
        data = serializer.data

        return Response(serializer.data, status=status.HTTP_200_OK)
