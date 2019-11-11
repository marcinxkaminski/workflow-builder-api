from os import environ

_TMP_PATH = 'tmp'

LOGGER = {
    'SAVE_TO_FILE': True,
    'PATH': './logs'
}

CDN = {
    'PATH': _TMP_PATH
}

CLEANER = {
    'AGE': 600,  # seconds
    'INTERVAL': 300,  # seconds
    'PATH': _TMP_PATH
}

BUILDER = {
    'PATH': 'components',
    'DEST_PATH': _TMP_PATH,
    'TEMPLATE_FILE': 'templates/workflow_main.py',
    'IMPORTS_COMMENT': 'IMPORTS',
    'MAIN_COMMENT': 'MAIN',
    'MAIN_FILE_NAME': 'main.py',
    'REQUIREMENTS_FILE_NAME': 'requirements.txt'
}

API = {
    'HOST': environ.get('HOST', '0.0.0.0'),
    'PORT': environ.get('PORT', '8000'),
    'TITLE': 'Workflow Builder',
    'DESCRIPTION': 'This app is Workflow Builder. It allows you to create any workflow by selecting the blocks in specified order, then you will get url to complete workflow file you could execute.',
    'BASE_PATH': '/api/workflow-builder{}',
    'ENDPOINTS': {
        'ELEMENTS': '/elements',
        'CDN': '/files'
    },
    'ORIGINS': ['*'],
    'METHODS': ['*'],
    'HEADERS': ['*'],
    'ALLOW_CREDENTIALS': False
}
