import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'your.domain.name',
]

# Leave this as true during development, so that you get error pages describing what went wrong
DEBUG = True

# You can add your e-mail if you want to receive notifications of failures I think , but its probably not a good idea
ADMINS = [
    # ('Your Name', 'your_email@example.com'),
]

# You can also make local sqlite databases in your current directory
# if you want to test changes to the data model
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

TIME_ZONE = 'America/Toronto'

# set this to your site's prefix, This allows handling multiple deployments from a common url base
SITE_PREFIX = ''

SECRET_KEY = 'IHaveNoIdeaWhatThisIsOrWhatItDoes'

STATIC_URL = "/static/" + SITE_PREFIX
STATIC_ROOT = os.path.join(BASE_DIR, 'static', SITE_PREFIX)

# Use this for running a separate beta testing site for people to generate beta seeds.
BETA = False
