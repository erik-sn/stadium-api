import logging
import ast
from typing import List, Dict, Any, Optional
import uuid

import requests
from django.shortcuts import get_object_or_404
from django.conf import settings
from social_django.models import UserSocialAuth

from stadium.users.models import User
from stadium.repositories.models import Repository
from stadium.repositories.utils import initialize_repo_from_json
from .errors import GithubException

logger = logging.getLogger('django')


class GithubApiClient:
    BASE_URL = 'https://api.github.com'

    access_token = None
    headers = {
        'Accept': 'application/json',
    }
    user = None

    def __init__(self, user: Optional[User]) -> None:
        if user:
            social_auth = get_object_or_404(UserSocialAuth, user=user)
            self.access_token = social_auth.extra_data['access_token']
            self.headers.update({'Authorization': f'token {self.access_token}'})
            self.user = user

    def repos(self):
        response = requests.get(f'{self.BASE_URL}/user/repos', headers=self.headers)
        if response.ok:
            return response.json()
        raise GithubException('Failed to retrieve user repos')

    def get(self, url, failure_message):
        response = requests.get(url, headers=self.headers)
        if response.ok:
            return response
        raise GithubException(failure_message)

    def get_access_token(self, code):
        state = uuid.uuid4()
        return requests.post('https://github.com/login/oauth/access_token', params={
            'client_id': settings.SOCIAL_AUTH_GITHUB_KEY,
            'client_secret': settings.SOCIAL_AUTH_GITHUB_SECRET,
            'code': code,
            'redirect_uri': settings.SOCIAL_AUTH_GITHUB_CALLBACK,
            'state': state,
        }, headers=self.headers)


class GithubUtils:

    def __init__(self, user):
        self.user = user
        self.client = GithubApiClient(user)

    def create_or_refresh_gym_repos(self) -> List[Repository]:
        valid_repos = []
        for repo in self.client.repos():

            ## base 64 encoded readme.md:
            response = requests.get(repo['contents_url'].replace('contents/{+path}', 'readme'), headers=self.client.headers)
            if response.ok:
                readme = response.json()
                repo.update({'readme': readme['content']})

            ## use application/vnd.github.VERSION.html in header:
            # header = self.client.headers
            # header.update({'Accept': 'application/vnd.github.v3.html'})
            # response = requests.get(repo['contents_url'].replace('contents/{+path}', 'readme'), headers=header)
            # if response.ok:
            #     readme = response.content
            #     # logger.info(f'readme: {readme.decode("utf-8")}')
            #     repo.update({'readme': readme.decode("utf-8")})

            ## use application/vnd.github.VERSION.raw in header:
            # header = self.client.headers
            # header.update({'Accept': 'application/vnd.github.v3.raw'})
            # response = requests.get(repo['contents_url'].replace('contents/{+path}', 'readme'), headers=header)
            # if response.ok:
            #     readme = response.content
            #     # logger.info(f'readme: {readme.decode("utf-8")}')
            #     repo.update({'readme': readme.decode("utf-8")})

            else:
                logger.info('Failed to included Readme.md.')
                repo.update({'readme': null})
            # TODO need to multi-thread this
            if self._is_gym_repo(repo['contents_url'].replace('{+path}', '')):
                repo.update({'gym': True})
            else:
                repo.update({'gym': False})
            valid_repos.append(repo)
        return [initialize_repo_from_json(repo, self.user) for repo in valid_repos]

    def _is_gym_repo(self, url: str):
        for file in self.client.get(url, f'Failed to retrieve contents from URL: {url}').json():
            if self._is_setup_py_file(file):
                logger.info(f'Found setup.py file in repo: {url}')
                return self._contains_gym_dependency(file)
        return False

    def _is_setup_py_file(self, file: Dict) -> bool:
        return file['name'] == 'setup.py'

    def _contains_gym_dependency(self, file: Dict) -> bool:
        """
        use ast (abstract syntax tree) to parse the setup.py python file and see if
        gym is listed as a dependency. We use this as our standard as indicated
        by open ai in their documentation:

        https://github.com/openai/gym/tree/master/gym/envs#how-to-create-new-environments-for-gym

        :param file:
        :return:
        """
        response = self.client.get(file['download_url'], 'Failed to retrieve file from github: {}'.format(file['name']))
        parsed = ast.parse(response.content)
        for index, node in enumerate(parsed.body[:]):
            try:
                if node.value.func.id == 'setup':
                    for kwarg in node.value.keywords:
                        if getattr(kwarg, 'arg', None) == 'install_requires':
                            return self._install_requires_gym(kwarg)
            except AttributeError:  # this occurs on any line where there's not a function declaration
                logger.debug('Skipping node index {} for file {}'.format(index, file['name']))
                continue

    def _install_requires_gym(self, kwarg: Any) -> bool:
        dependencies = getattr(getattr(kwarg, 'value'), 'elts')
        for dependency in dependencies:
            package_name = getattr(dependency, 's')  # I don't know why this is "s"!
            if 'gym' in package_name:  # TODO this is too naive, need to find a way to limit this to explicity gym
                return True
        return False


