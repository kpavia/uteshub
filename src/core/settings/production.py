import os
import dj_database_url
import json


CURRENT_SEASON = os.environ.get('CURRENT_SEASON')
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True if os.environ.get('DEBUG').lower() == 'true' else False

DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get('DATABASE_URL'))
DEFAULT_CONNECTION.update({'CONN_MAX_AGE': 600})
DATABASES = {
    'default': DEFAULT_CONNECTION
}

YT_API_KEY = os.environ.get('YT_API_KEY')
YT_EMBED_URL = os.environ.get('YT_EMBED_URL')
YT_SEARCH_URL = os.environ.get('YT_SEARCH_URL')
YT_CHANNEL_IDS = json.loads(os.environ.get('YT_CHANNEL_IDS'))
