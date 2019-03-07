from rest_framework import serializers

from scigym.images.models import Image, ImageUploadEvent




class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

class ImageUploadEventSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = ImageUploadEvent
        fields = ('id', 'image', 'description')
