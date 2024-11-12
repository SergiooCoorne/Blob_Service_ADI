import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
from blobservice.Presentation.presentation_blob import create_app, main

def run_server():
    app = create_app()
    main(app)