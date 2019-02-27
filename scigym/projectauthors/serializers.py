from rest_framework import serializers
from .models import ProjectAuthor


class ProjectAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectAuthor
        fields = '__all__'
