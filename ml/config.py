_TMP_PATH = './tmp'

CLEANER = {
    'AGE': 1800,  # seconds
    'INTERVAL': 300,  # seconds
    'PATH': _TMP_PATH
}

BUILDER = {
    'PATH': '/data',
    'DEST_PATH': _TMP_PATH
}

API = {
    'TITLE': 'ML Workflow Builder',
    'DESCRIPTION': 'This app is Machine Learning Workflow Builder. It allows you to create machine learning workflow by selecting the blocks in specified order, then you will get url to complete workflow file you could execute.',
    'BASE_PATH': '/api/workflow-builder{}',
    'ENDPOINTS': {
        'ELEMENTS': '/elements'
    }
}
