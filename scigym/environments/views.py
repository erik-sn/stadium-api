import logging
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from rest_framework import viewsets, status

from scigym.repositories.models import Repository
from .models import Environment, Topic
from .serializers import (
    EnvironmentSerializer,
    EnvironmentWriteSerializer,
    TopicSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from scigym.utils.helper import is_valid_uuid

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

        if is_valid_uuid(request.data['topic']):
            logger.info('valid UUID for topic')
            env.topic= Topic.objects.get(id=request.data['topic'])
            env.save()

        serializer = EnvironmentWriteSerializer(env)
        return Response(serializer.data, status=201)

    def delete(self, request, pk):
        '''
        Doesn't do anything
        '''
        env =  get_object_or_404(Environment, pk=pk)
        env.delete()
        return(Response(status=status.HTTP_204_NO_CONTENT))
    
    def update(self, request, pk):
        env =  get_object_or_404(Environment, pk=pk)
        env.name = request.data['name']
        env.description = request.data['description']
        env.tags = request.data['tags']
        if is_valid_uuid(request.data['topic']):
            logger.info('valid UUID for topic')
            env.topic = Topic.objects.get(id=request.data['topic'])
        else:
            env.topic = None
        env.save()
        serializer = EnvironmentWriteSerializer(env)
        return(Response(serializer.data, status=200))


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

    @action(['GET'], detail=False)
    def filter_topic(self, request):
        from django.db.models import Q

        search_term = request.GET.get('topic', '')

        if len(search_term) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # here we look for both the parent topic and the child topic
        search_query = Q(topic__exact=search_term) | Q(topic__parent_topic__exact=search_term)
        test_query = Q(topic__parent_topic__exact=search_term)
        logger.debug(search_query)
        logger.info(test_query)
        environments = Environment.objects.filter(search_query).select_related('repository')
        environments_test = Environment.objects.filter(test_query).select_related('repository')
        logger.info(environments_test)
        serializer = EnvironmentSerializer(environments, many=True)
        data = serializer.data

        return Response(serializer.data, status=status.HTTP_200_OK)
        
class TopicViewSet(viewsets.ModelViewSet):
    """
    View to create topics
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def create(self, request) -> Response:

        try:
            parent=Topic.objects.filter(name=request.data['parent_topic'])[0]
            topic = Topic.objects.create(
                name=request.data['name'],
                parent_topic=parent
            )
            topic.save()
            serializer = TopicSerializer(topic)
            return Response(serializer.data, status=201)
        except:
            response = super(TopicViewSet, self).create(request)
            return response
