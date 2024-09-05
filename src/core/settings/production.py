import os
import dj_database_url


CURRENT_SEASON = os.environ.get('CURRENT_SEASON')
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True if os.environ.get('DEBUG').lower() == 'true' else False

DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get('DATABASE_URL'))
DEFAULT_CONNECTION.update({'CONN_MAX_AGE': 600})
DATABASES = {
    'default': DEFAULT_CONNECTION
}
