from os import environ

_MODULE_PATH = "./wb"
_TMP_PATH = "tmp"

LOGGER = {"SAVE_TO_FILE": True, "PATH": f"{_MODULE_PATH}/logs"}

CDN = {"PATH": f"{_MODULE_PATH}/{_TMP_PATH}", "WORKFLOW_FILENAME": "workflow"}

CLEANER = {
    "AGE": 600,
    "INTERVAL": 300,
    "PATH": f"{_MODULE_PATH}/{_TMP_PATH}",
}  # seconds  # seconds

BUILDER = {
    "PATH": f"{_MODULE_PATH}/components",
    "DEST_PATH": f"{_MODULE_PATH}/{_TMP_PATH}",
    "TEMPLATE_FILE": f"{_MODULE_PATH}/templates/workflow_main.py",
    "IMPORTS_COMMENT": "IMPORTS",
    "MAIN_COMMENT": "MAIN",
    "MAIN_FILE_NAME": "main.py",
    "REQUIREMENTS_FILE_NAME": "requirements.txt",
}

API = {
    "HOST": environ.get("HOST"),
    "PORT": environ.get("PORT", "8000"),
    "TITLE": "Workflow Builder",
    "DESCRIPTION": "This app is Workflow Builder. It allows you to create any workflow by selecting the blocks in specified order, then you will get url to complete workflow file you could execute.",
    "BASE_PATH": "/api/workflow-builder{}",
    "ENDPOINTS": {"ELEMENTS": "/elements", "CDN": "/files"},
    "ORIGINS": ["https://workflowbuilder.netlify.com"],
    "METHODS": ["GET", "PUT", "POST"],
    "HEADERS": ["*"],
    "ALLOW_CREDENTIALS": False,
}
