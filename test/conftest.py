import pytest
import os
from blobservice.Presentation.presentation_blob import create_app

def pytest_addoption(parser):
    parser.addoption("--port", action="store", help="Número de puerto")
    parser.addoption("--listening", action="store", help="Dirección donde se producirá la escucha")
    parser.addoption("--storage", action="store", help="Ruta de almacenamiento")

@pytest.fixture
def client(request):
    port = request.config.getoption("--port") or 1234
    listening = request.config.getoption("--listening") or "localhost"
    storage = request.config.getoption("--storage") or "/home/sergio"

    os.environ["APP_PORT"] = str(port)
    os.environ["APP_LISTENING"] = listening
    os.environ["APP_STORAGE"] = storage

    app = create_app()

    with app.test_client() as client:
        yield client