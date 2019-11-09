from os import environ

_TMP_PATH = './tmp'

LOGGER = {
    'PATH': './logs'
}

CLEANER = {
    'AGE': 1800,  # seconds
    'INTERVAL': 300,  # seconds
    'PATH': _TMP_PATH
}

BUILDER = {
    'PATH': './components',
    'DEST_PATH': _TMP_PATH
}

API = {
    'HOST': environ.get('HOST', '0.0.0.0'),
    'PORT': environ.get('PORT', '0.0.0.0'),
    'TITLE': 'Workflow Builder',
    'DESCRIPTION': 'This app is Workflow Builder. It allows you to create any workflow by selecting the blocks in specified order, then you will get url to complete workflow file you could execute.',
    'BASE_PATH': '/api/workflow-builder{}',
    'ENDPOINTS': {
        'ELEMENTS': '/elements',
        'FILES': '/files'
    }
}
