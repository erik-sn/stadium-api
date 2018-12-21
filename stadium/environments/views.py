import logging
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view

from stadium.repositories.models import Repository
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
    permission_classes = (IsOwnerOrReadOnly,)#(AllowAny,)

    def get_serializer_class(self):
        return EnvironmentWriteSerializer if self.request.method in WRITE_VERBS else self.serializer_class
    
    # @permission_classes((AllowAny, ))
    # def get(self, request):
    #     environments = Environment.objects.all()
    #     return Response(EnvironmentSerializer(environments, many=True).data, status=status.HTTP_200_OK)

    
    # @permission_classes((IsAuthenticated, ))
    def create(self, request):
        env = Environment.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            repository=Repository.objects.get(id=request.data['repository']),
            tags=request.data['tags']
        )
        serializer = EnvironmentWriteSerializer(env)
        return Response(serializer.data, status=201)

    # @permission_classes((IsAuthenticated, ))
    def delete(self, request, pk):
        env =  get_object_or_404(pk)
        env.delete()
        return(Response(status=status.HTTP_204_NO_CONTENT))