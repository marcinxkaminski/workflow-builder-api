_TMP_PATH = '/tmp'

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
    'NAME': 'Machine Learning Workflow Builder',
    'ALLOWED_METHODS': ['GET', 'POST'],
    'ENDPOINTS': {
        'WORKFLOW_BUILDER': '/workflow-builder'
    }
}
