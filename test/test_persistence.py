from src.Persistence.persistence_blob import Blob, Persistence, BlobNotFound
import pytest
import os

@pytest.fixture
def blob_created():
    blob_created = Blob('Test_1', 'owner_1',['rol_test1', 'rol_test_2'], 'Test_Create_blob'.encode())
    yield blob_created
    
@pytest.fixture
def blob():
    obj = Persistence()
    blob_id, rtr = obj.create_blob('Test_1', 'owner_1', ['rol_test1', 'rol_test_2'], 'Test_Create_blob'.encode())
    yield obj, blob_id, rtr
    
@pytest.fixture(scope='session', autouse = True)
def cleanup_json_file():
    yield
    if os.path.exists('./test/json_test.json'):
        os.remove('./test/json_test.json')
    
def test_atributes_blob_(blob_created):
    instance_blob = blob_created
    assert instance_blob.get_blob_id is not None
    assert instance_blob.get_blob_name is not None
    assert instance_blob.get_blob_owner is not None
    assert instance_blob.get_blob_roles is not None
    assert instance_blob.get_blob_data is not None    
    
def test_create_blob(blob):
    obj, blob_id, rtr = blob
    assert blob_id is not None
    assert rtr is True
    
def test_get_data_blob(blob):
    obj, blob_id, rtr = blob

    data = obj.get_data_blob(blob_id)
    assert data is not None
    
def test_get_name_blob(blob):
    obj, blob_id, rtr = blob

    name = obj.get_name_blob(blob_id)
    assert name is not None
    
def test_get_owner_blob(blob):
    obj, blob_id, rtr = blob

    owner = obj.get_owner_blob(blob_id)
    assert owner is not None
    
def test_get_roles_blob(blob):
    obj, blob_id, rtr = blob

    roles = obj.get_roles_blob(blob_id)
    assert roles is not None

def test_delete_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.delete_blob(blob_id)

    assert rtr is True
    
def test_modify_data_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_data_blob(blob_id, 'Test_Modify_Data'.encode())

    assert rtr is True
    
def test_modify_name_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_name_blob(blob_id, 'Test_Modify_Name')

    assert rtr is True
    
def test_modify_owner_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_owner_blob(blob_id, 'Test_Modify_Owner')

    assert rtr is True
    
def test_modify_roles_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_roles_blob(blob_id, ['rol_test1', 'rol_test_2', 'rol_test_3'])

    assert rtr is True
    
def test_exception_get_data_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.get_data_blob(blob_id)    
        
def test_exception_get_name_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.get_name_blob(blob_id) 
        
def test_exception_get_owner_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.get_owner_blob(blob_id)   
        
def test_exception_get_roles_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.get_roles_blob(blob_id)
        
def test_exception_detele_blob(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.delete_blob(blob_id)
        
def test_exception_modify_data_blob(blob):
    obj, blob_id, rtr = blob
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{4378294}' no encontrado"):
        obj.modify_data_blob('4378294', 'Test_Modify_Data'.encode())
        
def test_exception_modify_name_blob(blob):
    obj, blob_id, rtr = blob
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{4378294}' no encontrado"):
        obj.modify_name_blob('4378294', 'Test_Modify_Name')
        
def test_exception_modify_owner_blob(blob):
    obj, blob_id, rtr = blob
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{4378294}' no encontrado"):
        obj.modify_owner_blob('4378294', 'Test_Modify_Owner')
        
def test_exception_modify_roles_blob(blob):
    obj, blob_id, rtr = blob
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{4378294}' no encontrado"):
        obj.modify_roles_blob('4378294', ['rol_test1', 'rol_test_2', 'rol_test_3'])