import logging
import re
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from rest_framework import viewsets, status

from scigym.repositories.models import Repository
from .models import Environment, Topic, Image
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

        # get image
        if is_valid_uuid(request.data['avatar']):
            avatar = Image.objects.get(id=request.data['avatar'])
        else:
            avatar = None
        env_name = request.data['name']
        env_name = re.sub(' {2,}', '-', env_name)
        env = Environment.objects.create(
            name=env_name,
            description=request.data['description'],
            repository=Repository.objects.get(id=request.data['repository']),
            tags=request.data['tags'],
            current_avatar=avatar
        )

        if is_valid_uuid(request.data['topic']):
            logger.info('valid UUID for topic')
            env.topic= Topic.objects.get(id=request.data['topic'])
            env.save()

        serializer = EnvironmentWriteSerializer(env)
        return Response(serializer.data, status=201)
    
    def update(self, request, pk):
        env =  get_object_or_404(Environment, pk=pk)
        env_name = request.data['name']
        env_name = re.sub(' {2,}', '-', env_name)
        env.name = env_name
        env.description = request.data['description']
        env.tags = request.data['tags']
        logger.info(request.data)
        if is_valid_uuid(request.data['topic']):
            logger.info('valid UUID for topic')
            env.topic = Topic.objects.get(id=request.data['topic'])
        else:
            env.topic = None
        if is_valid_uuid(request.data['avatar_id']):
            logger.info('valid UUID for avatar')
            env.current_avatar = Image.objects.get(id=request.data['avatar_id'])
        else:
            env.current_avatar = None
        env.save()
        serializer = EnvironmentWriteSerializer(env)
        return(Response(serializer.data, status=200))


    @action(['GET'], detail=False)
    def filter(self, request):

        from django.db.models import Q

        search_terms = request.GET.get('search', '').split(',')
        if len(search_terms) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for i, term in enumerate(search_terms):
            if i == 0:
                search_query = Q(name__icontains=term) | Q(tags__icontains=term) | Q(topic__name__icontains=term)
            else:
                search_query |= Q(name__icontains=term)
                search_query |= Q(tags__icontains=term)
                search_query |= Q(topic__name__icontains=term)
        logger.debug(search_query)

        environments = Environment.objects.filter(search_query).select_related('repository')

        serializer = EnvironmentSerializer(environments, many=True)
        data = serializer.data

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=False)
    def filter_topic(self, request):
        from django.db.models import Q

        search_term = request.GET.get('topic', '')

        if len(search_term) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # here we look for both the parent topic and the child topic (UUID)
        search_query = Q(topic__exact=search_term) | Q(topic__parent_topic__exact=search_term)
        logger.debug(search_query)

        environments = Environment.objects.filter(search_query).select_related('repository')
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
