import logging

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from django import forms

from .permissions import IsOwnerOrReadOnly
from scigym.images.utils import save_image
from scigym.images.models import Image
from scigym.images.serializers import ImageSerializer

logger = logging.getLogger('django')


class UploadImageForm(forms.Form):
    file = forms.ImageField()


class ImageViewSet(viewsets.ModelViewSet):
    """
    View to create images and save them to the filesystem  
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsOwnerOrReadOnly,)

    @action(['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def mine(self, request):
        images = Image.objects.filter(owner=request.user)
        return Response(ImageSerializer(images, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        form: UploadImageForm = UploadImageForm(request.POST, request.FILES)

        if form.is_valid():

            file: InMemoryUploadedFile = request.FILES['file']

            saved_image = save_image(file, request.user)

            serializer = ImageSerializer(saved_image)
            return Response(serializer.data, status=201)

        return Response(form.errors, status=400)
