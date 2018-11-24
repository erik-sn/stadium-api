from rest_framework import serializers
from .models import Environment, Repository

from stadium.users.serializers import UserSerializer


class RepositorySerializer(serializers.ModelSerializer):
    owner = UserSerializer()  # TODO groups can own this too

    class Meta:
        model = Repository
        depth = 1
        fields = ('id', 'name', 'description', 'owner', 'homepage', 'private', 'fork', 'size',
                  'forks', 'stargazers_count', 'license', 'api_url', 'html_url', 'ssh_url', 'git_url', 'readme',
                  'pypi_url', 'pypi_name')


class EnvironmentSerializer(serializers.ModelSerializer):
    repository = RepositorySerializer()

    class Meta:
        model = Environment
        depth = 1
        fields = '__all__'
