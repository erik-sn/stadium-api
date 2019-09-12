import logging
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import viewsets, status

from scigym.environments.models import Environment
from scigym.users.models import User
from .models import MessageBoard, Comment
from .serializers import (
    MessageBoardSerializer,
    MessageBoardWriteSerializer,
    CommentSerializer
)

logger = logging.getLogger('django')

WRITE_VERBS = ['POST', 'PUT']

class MessageBoardViewSet(viewsets.ModelViewSet):
    """
    View to create message boards
    """
    queryset = MessageBoard.objects.all()
    serializer_class = MessageBoardSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return MessageBoardWriteSerializer if self.request.method in WRITE_VERBS else self.serializer_class
    
    def create(self, request, *args, **kwargs):

        board_data = {
            'title': request.data['title'],
            'description': request.data['description'],
            'tags': request.data['tags']
        }

        serializer = MessageBoardWriteSerializer(data=board_data)
        if serializer.is_valid(raise_exception=True):
            author = get_object_or_404(User, id=request.user.id)
            env = get_object_or_404(Environment, id=request.data['environment'])
            logger.info(env)
            logger.info(author)
            board = MessageBoard.objects.create(
                title=board_data['title'],
                description=board_data['description'],
                tags=board_data['tags'],
                author=author,
                environment=env
            )

            board.save()

            return Response(serializer.data, status=201)
