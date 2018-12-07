import logging
from typing import Dict

from stadium.users.models import User
from stadium.repositories.models import Repository
from stadium.utils.errors import GithubException

logger = logging.getLogger('django')


def initialize_repo_from_json(json: Dict, owner: User) -> Repository:
    try:
        github_id = json['id']
        transformed_json = {
            'name': json['name'],
            'full_name': json['full_name'],
            'homepage': json['homepage'],
            'description': json['description'],
            'private': json['private'],
            'fork': json['fork'],
            'size': json['size'],
            'stargazers_count': json['stargazers_count'],
            'forks': json['forks'],
            'watchers': json['watchers'],
            'html_url': json['html_url'],
            'ssh_url': json['ssh_url'],
            'git_url': json['git_url'],
            'raw_api_response': json,

            'api_url': json['url'],
            'github_id': github_id,
            'license': json['license']['name'] if json['license'] else None,
            'owner': owner,
            # 'readme': ???  # TODO implement this
        }
        if Repository.objects.filter(github_id=github_id).exists():
            # TODO test that this actually works on a real repo!!
            logger.info('Updating existing repo {} with github ID {}'.format(json['name'], github_id))
            Repository.objects.filter(github_id=github_id).update(**transformed_json)
            return Repository.objects.get(github_id=github_id)
        else:
            logger.info('Creating new repo {} with github ID {}'.format(json['name'], github_id))
            return Repository.objects.create(**transformed_json)

    except KeyError:
        logger.exception('message')
        raise GithubException('Error extracting github repository data into model')
