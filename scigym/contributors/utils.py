import logging
from typing import Dict

from scigym.users.models import User
from scigym.contributors.models import Contributor
from scigym.utils.errors import GithubException

logger = logging.getLogger('django')


def initialize_contributor_from_json(json: Dict) -> Contributor:
    logger.info(json)
    try:
        github_id = json['id']
        transformed_json = {
            'login': json['login'],
            'html_url': json['html_url'],
            'avatar_url': json['avatar_url'],
            'github_id': github_id,
            'contributions': json['contributions']
        }
        if Contributor.objects.filter(github_id=github_id).exists():
            logger.info('Updating existing Contributor {} with github ID {}'.format(json['login'], github_id))
            Contributor.objects.filter(github_id=github_id).update(**transformed_json)
            return Contributor.objects.get(github_id=github_id)
        else:
            logger.info('Creating new contributor {} with github ID {}'.format(json['login'], github_id))
            return Contributor.objects.create(**transformed_json)

    except KeyError:
        logger.exception('message')
        raise GithubException('Error extracting github repository data into model')
