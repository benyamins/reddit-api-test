import sys
from typing import Dict, Any, Union
from configparser import ConfigParser
from pathlib import Path, PosixPath
from logging import DEBUG

LOGGING_LEVEL = DEBUG

MODULE_PATH: PosixPath = Path(__file__).parent.absolute()

DATABASE = MODULE_PATH / 'reddit.db'

# ==== Confing File ==== #

CONFIG_FILE_PATH: PosixPath = MODULE_PATH / 'conf.ini'
config = ConfigParser()

try:
    config.read(CONFIG_FILE_PATH)
except FileNotFoundError as err:
    print('conf.ini was not found')
    sys.exit(1)


REDDIT_URL = 'https://www.reddit.com'
REDDIT_AUTH_URL = 'https://oauth.reddit.com'

SUPPORTED_SECTIONS = [
    'overview',
    'submitted',
    'upvoted',
    'downvoted',
    'hidden',
    'saved',
    'gilded',
]


if __name__ == '__main__':
    from pprint import pprint
    print(MODULE_PATH)
    # pprint(payload, indent=2)
