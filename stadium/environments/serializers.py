from rest_framework import serializers
from .models import Environment

from stadium.users.serializers import UserSerializer
from stadium.repositories.serializers import RepositorySerializer


class EnvironmentSerializer(serializers.ModelSerializer):
    repository = RepositorySerializer(read_only=True)

    class Meta:
        model = Environment
        depth = 1
        fields = ('id', 'name', 'description', 'repository')

class EnvironmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Environment
        depth = 1
        fields = ('id', 'name', 'description', 'repository')