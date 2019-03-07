import logging
import os
import magic

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from django import forms
from django.views.generic import View
from django.http import HttpResponse

from scigym.images.utils import save_image, delete_image
from scigym.images.models import Image, ImageUploadEvent
from scigym.images.serializers import ImageSerializer, ImageUploadEventSerializer

logger = logging.getLogger('django')

class UploadImageForm(forms.Form):
    file = forms.ImageField()

class ImageViewSet(viewsets.ModelViewSet):
    """
    View to create images
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (AllowAny,) # TODO add isUserOrReadOnly permissions

    def destroy(self, request, *args, **kwargs):
        image = self.get_object()
        delete_image(image.file_path)
        self.perform_destroy(image)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ImageUploadEventViewSet(viewsets.ModelViewSet):
    """
    View to process an image upload event, saving an image to the filesystem
    """
    queryset = ImageUploadEvent.objects.all()
    serializer_class = ImageUploadEventSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny,) # TODO add isUserOrReadOnly permissions

    def create(self, request, *args, **kwargs):
        form: UploadImageForm = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            file: InMemoryUploadedFile = request.FILES['file']
            try:
                description_txt = request.POST['description']
                saved_file = save_image(file, description_txt)
            except:
                description_txt = ""
                saved_file = save_image(file, description_txt)
            if len(saved_file) == 0:
                return Response(form.errors, status=400)
            upload_event = ImageUploadEvent.objects.create(
                file_name=file.name,
                description=description_txt
                )
            
            upload_event.image.set(saved_file)
            upload_event.save()

            serializer = ImageUploadEventSerializer(upload_event)
            return Response(serializer.data, status=201)

        return Response(form.errors, status=400)
