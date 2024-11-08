from src.Persistence.persistence_blob import Blob, Persistence, BlobNotFound
import pytest
import shutil
import os
from unittest.mock import Mock    

@pytest.fixture(scope='session', autouse=True)
def setup_and_cleanup():
    # Define el nombre del directorio donde se guardarán los archivos
    test_dir = './test/data_directory'
    # Crea el directorio si no existe
    os.makedirs(test_dir, exist_ok=True)
    
    #Definicion de archivos para testear 
    test_file = os.path.join(test_dir, 'test_file.txt')
    json_file = os.path.join(test_dir, 'json_test.json')

    #Creacion del archivo donde se guardaran los Blobs
    with open(json_file, 'w') as f:
        f.write('{}')

    #Creacion del archivo para asociarlo a un Blob
    with open(test_file, 'w') as f:
        f.write('Test')

    yield test_dir, test_file, json_file

    # Al finalizar los tests, eliminamos el directorio y todo su contenido
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

@pytest.fixture
def blob_created(setup_and_cleanup):
    test_dir, test_file, json_file = setup_and_cleanup

    blob_created = Blob('blob_name', 'owner_1',['rol_test1', 'rol_test_2'], 'test_path')
    yield blob_created
    
@pytest.fixture
def blob(setup_and_cleanup):
    test_dir, test_file, json_file = setup_and_cleanup

    # Creacion de mock para poder usar el metodo save correctamente (Lo ejecuta la capa de persistencia)
    mock_file = Mock()
    mock_file.save = Mock()

    obj = Persistence(test_dir)
    blob_id, rtr = obj.create_blob('blob_name', 'owner_1',['rol_test1', 'rol_test_2'], test_file, mock_file)
    yield obj, blob_id, rtr

def test_blob_exits_True(blob):
    obj, blob_id, rtr = blob

    assert obj.blob_exits(blob_id) is True

def test_blob_exits_False(blob):
    obj, blob_id, rtr = blob

    blob_id = 'dbjqkbdiq'
    with pytest.raises(BlobNotFound, match=f"Blob con ID '{blob_id}' no encontrado"):
        obj.blob_exits(blob_id)  

def test_atributes_blob_(blob_created):
    instance_blob = blob_created
    assert instance_blob.get_blob_id is not None
    assert instance_blob.get_blob_name is not None
    assert instance_blob.get_blob_owner is not None
    assert instance_blob.get_path_file_blob is not None   
    assert instance_blob.get_blob_roles is not None
     
def test_create_blob(blob):
    obj, blob_id, rtr = blob
    assert blob_id is not None
    assert rtr is True
    
def test_get_path_file_blob(blob):
    obj, blob_id, rtr = blob

    path = obj.get_path_file_blob(blob_id)
    assert path is not None
    
def test_get_name_blob(blob):
    obj, blob_id, rtr = blob

    name = obj.get_name_blob(blob_id)
    assert name is not None
        
def test_get_roles_blob(blob):
    obj, blob_id, rtr = blob

    roles = obj.get_roles_blob(blob_id)
    assert roles is not None

def test_delete_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.delete_blob(blob_id)

    assert rtr is True
        
def test_modify_file_blob(blob, setup_and_cleanup):
    obj, blob_id, rtr = blob
    test_dir, test_file, json_file = setup_and_cleanup

    mock_file = Mock()
    mock_file.save = Mock()
    mock_file.filename = "test_file.txt" 
    
    rtr = obj.modify_file_blob(blob_id, mock_file, test_dir)

    assert rtr is True
    
def test_modify_name_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_name_blob(blob_id, 'Test_Modify_Name')

    assert rtr is True
        
def test_modify_roles_blob(blob):
    obj, blob_id, rtr = blob

    rtr = obj.modify_roles_blob(blob_id, ['rol_test1', 'rol_test_2', 'rol_test_3'])

    assert rtr is True