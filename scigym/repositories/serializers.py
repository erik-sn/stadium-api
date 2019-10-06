from rest_framework import serializers
from .models import Repository

from scigym.users.serializers import UserSerializer


class RepositorySerializer(serializers.ModelSerializer):
    owner = UserSerializer()  # TODO groups can own this too

    class Meta:
        model = Repository
        depth = 1
        fields = ('id', 'name', 'description', 'owner', 'homepage', 'private', 'fork', 'size',
                  'forks', 'stargazers_count', 'license', 'api_url', 'html_url', 'ssh_url',
                  'git_url', 'readme', 'readme_name', 'pypi_name', 'gym')

