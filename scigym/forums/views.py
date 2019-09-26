import logging
import re
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
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
        board_title = request.data['title']
        # convert spaces to dashes.
        board_title_url = re.sub(' {1,}', '-', board_title).replace('?', '%3F')
        env = get_object_or_404(Environment, id=request.data['environment'])
        # add full url
        board_title_url = '/env/'+env.url+'/forum/'+board_title_url

        board_data = {
            'title': board_title,
            'title_url': board_title_url,
            'description': request.data['description'],
            'tags': request.data['tags']
        }

        serializer = MessageBoardWriteSerializer(data=board_data)
        if serializer.is_valid(raise_exception=True):
            author = get_object_or_404(User, id=request.user.id)
            board = MessageBoard.objects.create(
                title=board_data['title'],
                title_url=board_data['title_url'],
                description=board_data['description'],
                tags=board_data['tags'],
                author=author,
                environment=env
            )

            board.save()

            return Response(serializer.data, status=201)

    def update(self, request, pk):
        board =  get_object_or_404(MessageBoard, pk=pk)
        board_title = request.data['title']
        # convert spaces to dashes.
        board_title_url = re.sub(' {1,}', '-', board_title)
        # add full url
        board_title_url = '/env/'+board.environment.url+'/forum/'+board_title_url

        board_data = {
            'title': board_title,
            'title_url': board_title_url,
            'description': request.data['description'],
            'tags': request.data['tags']
        }

        serializer = MessageBoardSerializer(board, data=board_data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            return(Response(serializer.data, status=200))

class CommentViewSet(viewsets.ModelViewSet):
    """
    View to create Comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        comment_data = {
            'comment': request.data['comment'],
        }

        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid(raise_exception=True):
            author = get_object_or_404(User, id=request.user.id)
            messageboard = get_object_or_404(MessageBoard, id=request.data['messageboard'])
            logger.info(messageboard)
            comment = Comment.objects.create(
                comment=comment_data['comment'],
                author=author,
                board=messageboard
            )

            comment.save()

            return Response(serializer.data, status=201)

    def update(self, request, pk):
        comment =  get_object_or_404(Comment, pk=pk)

        comment_data = {
            'comment': request.data['comment'],
        }

        serializer = CommentSerializer(comment, data=comment_data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            return(Response(serializer.data, status=200))

    @action(['GET'], detail=False)
    def count_comments(self, request):
        messageboards = MessageBoard.objects.all()
        data = {}
        for board in messageboards:
            comments = Comment.objects.filter(board=board.id)
            data[str(board.id)] = len(comments)
        return Response(data, status=status.HTTP_200_OK)
    
    @action(['GET'], detail=False)
    def board_comments(self, request):
        board_id = request.GET.get('messageboard', '')
        comments = Comment.objects.filter(board=board_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
