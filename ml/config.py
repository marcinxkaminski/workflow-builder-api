from os import environ

_TMP_PATH = './tmp'

LOGGER = {
    'PATH': './logs'
}

CLEANER = {
    'AGE': 600,  # seconds
    'INTERVAL': 300,  # seconds
    'PATH': _TMP_PATH
}

BUILDER = {
    'PATH': './components',
    'DEST_PATH': _TMP_PATH,
    'TEMPLATE_FILE': './templates/workflow_main.py'
    'IMPORTS_COMMENT': '# IMPORTS',
    'MAIN_COMMENT': '# MAIN'
}

API = {
    'HOST': environ.get('HOST', '0.0.0.0'),
    'PORT': environ.get('PORT', '8080'),
    'TITLE': 'Workflow Builder',
    'DESCRIPTION': 'This app is Workflow Builder. It allows you to create any workflow by selecting the blocks in specified order, then you will get url to complete workflow file you could execute.',
    'BASE_PATH': '/api/workflow-builder{}',
    'ENDPOINTS': {
        'ELEMENTS': '/elements'
    },
    'ORIGINS': ['http://localhost:8080', 'https://localhost:8080', 'https://xkamson.github.io/ml-web/'],
    'METHODS': ['GET', 'PUT', 'POST'],
}
