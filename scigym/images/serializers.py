from rest_framework import serializers

from scigym.images.models import Image




class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
