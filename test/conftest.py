def pytest_addoption(parser):
    parser.addoption("--port", action="store", help="Número de puerto")
    parser.addoption("--listening", action="store", help="Dirección donde se producirá la escucha")
    parser.addoption("--storage", action="store", help="Ruta de almacenamiento")
