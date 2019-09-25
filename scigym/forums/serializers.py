from rest_framework import serializers
from .models import MessageBoard, Comment

from scigym.users.serializers import UserSerializer
from scigym.environments.serializers import EnvironmentSerializer

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        depth = 1
        fields = '__all__'

class MessageBoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    environment = EnvironmentSerializer(read_only=True)

    class Meta:
        model = MessageBoard
        depth = 1
        fields = '__all__'


class MessageBoardWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageBoard
        depth = 1
        fields = '__all__'
