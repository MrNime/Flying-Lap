import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT= os.path.join(PROJECT_DIR,'staticfiles/')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT,'Flying Lap/static/'),
)
