from rest_framework import serializers
from rest_framework.exceptions import ValidationError, _get_error_details
from .models import Environment, Topic
import logging

from scigym.users.serializers import UserSerializer
from scigym.repositories.serializers import RepositorySerializer
from scigym.images.serializers import ImageSerializer

logger = logging.getLogger('django')

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

class EnvironmentFormSerializer(serializers.ModelSerializer):

    def is_valid_form(self, raise_exception=False):
        """
        The same as `.is_valid()` but with any error `code='unique'` removed.
        This is used to validate data that is being edited.
        """
        assert not hasattr(self, 'restore_object'), (
            'Serializer `%s.%s` has old-style version 2 `.restore_object()` '
            'that is no longer compatible with REST framework 3. '
            'Use the new-style `.create()` and `.update()` methods instead.' %
            (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        self._remove_errors()

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)
    
    def _remove_errors(self):
        """
        Removes errors of type `code='unique'` from specified errors.

        TODO: Use code.
        """
        if 'name' in self.errors.keys():
            for error in self.errors['name']:
                if error == 'environment with this name already exists.':
                    error_detail = self._errors.pop('name')
                    logger.info(f'Removing some `unique` errors: {error_detail}')

    class Meta:
        model = Environment
        depth = 1
        fields = ('id', 'name', 'description', 'tags', 'topic', 'current_avatar')
