import logging
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from rest_framework import viewsets, status

from stadium.repositories.models import Repository
from .models import Environment
from .serializers import (
    EnvironmentSerializer,
    EnvironmentWriteSerializer
)
from .permissions import IsOwnerOrReadOnly

"""
UI
- input field (search happens)
- after the user types some characters (3 or more) then we call the API for a search
    - Debounce
        - debounce(call_search_api, 500)
        - user types in mario very quickly
            - 1 API call
- once we get the API call results display in a dropdown beneath the input field

API
- In a view implement the filter
- typically with query parameters /environments?name=mario&tags=test,python,javascript&owner=erik
"""

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
        # User.objects.filter(Q(income__gte=5000) | Q(income__isnull=True))

        # /api/v1/environments/filter/
        # python erik
        # http://0.0.0.0:8000/api/v1/environments/filter/?search=mario,python
        search_terms = request.GET.get('search', '').split(',')
        if len(search_terms) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        logger.info(search_terms)
        """
        condition = Q(full_name__icontains=s[0])
        for string in strings[1:]:
            condition &= Q(full_name__icontains=string)
        queryset = Profile.objects.filter(condition) 
        """
        # Environment.objects.filter(name__isnull=False)

        query = Q(name__isnull=False)  # initialize the query with a condition we always know is true
        for term in search_terms:
            query &= Q(name__icontains=term) # | Q(tags__contains=[term])  # TODO turn on tag filtering

        logger.debug(query)

        environments = Environment.objects.filter(query).select_related('repository')

        serializer = EnvironmentSerializer(environments, many=True)
        data = serializer.data
        logger.info(len(data))
        return Response(serializer.data, status=status.HTTP_200_OK)
