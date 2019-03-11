from rest_framework import serializers
from .models import Environment, Topic

from scigym.users.serializers import UserSerializer
from scigym.repositories.serializers import RepositorySerializer
from scigym.images.serializers import ImageSerializer


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        depth = 1
        fields = '__all__'

class EnvironmentSerializer(serializers.ModelSerializer):
    repository = RepositorySerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    current_avatar = ImageSerializer(read_only=True)

    class Meta:
        model = Environment
        depth = 1
        fields = ('id', 'name', 'description', 'scigym', 'repository', 'tags', 'topic', 'current_avatar')


class EnvironmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Environment
        depth = 1
        fields = ('id', 'name', 'description', 'repository', 'tags', 'topic', 'current_avatar')
