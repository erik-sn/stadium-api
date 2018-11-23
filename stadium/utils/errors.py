from rest_framework import status
from rest_framework.response import Response


def internal_error(key: str, description: str, status: int = status.HTTP_400_BAD_REQUEST):
    return Response({'error': key, 'error_description': description}, status=status)


class GithubException(Exception):
    pass
