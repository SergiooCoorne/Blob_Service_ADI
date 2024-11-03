from src.Persistence.persistence_blob import Blob, Persistence, BlobNotFound
import pytest
import os

@pytest.fixture
def blob_created():
    blob_created = Blob('Test_1', ['rol_test1', 'rol_test_2'], 'Test_Create_blob'.encode())
    yield blob_created

def test_blob_1(blob_created):
    instance_blob = blob_created
    assert instance_blob.get_blob_id is not None
    assert instance_blob.get_blob_name is not None
    assert instance_blob.get_blob_roles is not None
    assert instance_blob.get_blob_data is not None    

@pytest.fixture
def blob():
    obj = Persistence()
    blob_id, rtr = obj.create_blob('Test_1', ['rol_test1', 'rol_test_2'], 'Test_Create_blob'.encode())
    yield obj, blob_id, rtr

@pytest.fixture(scope='session', autouse = True)
def cleanup_json_file():
    yield
    if os.path.exists('./test/json_test.json'):
        os.remove('./test/json_test.json')

def test_create_blob(blob):
    obj, blob_id, rtr = blob
    assert blob_id is not None
    assert rtr is True

def test_1_get_data(blob):
    obj, blob_id, rtr = blob

    data = obj.get_blob_data(blob_id)
    assert data is not None

def test_2_get_data(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.get_blob_data(blob_id)

def test_delete_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.delete_blob(blob_id)

    assert rtr is True

def test_2_detele_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.delete_blob(blob_id)

def test_1_modify_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_blob(blob_id, 'Blob_Test_Modified', ['rol_test1_modified', 'rol_test2_modified'], new_data = 'Test_Create_blob_Modified'.encode())
    assert rtr is True

def test_2_modify_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'

    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
       obj.modify_blob(blob_id, 'Blob_Test_Modified', ['rol_test1_modified', 'rol_test2_modified'], new_data = 'Test_Create_blob_Modified'.encode())