from rest_framework import serializers
from .models import Repo

from stadium.users.serializers import UserSerializer


class RepoSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Repo
        depth = 1
        fields = ('id', 'name', 'description', 'owner', 'homepage', 'private', 'fork', 'size',
                  'forks', 'stargazers_count', 'license', 'api_url', 'html_url', 'ssh_url', 'git_url', 'readme',
                  'pypi_url', 'pypi_name')

