from src.Business.business_blob import Business, Forbidden
from src.Persistence.persistence_blob import Blob
import pytest
import shutil
import os
from unittest.mock import Mock  
from werkzeug.datastructures import FileStorage

@pytest.fixture(scope='session', autouse=True)
def setup_and_cleanup():
    # Define el nombre del directorio donde se guardarán los archivos
    test_dir = './test/data_directory'
    # Crea el directorio si no existe
    os.makedirs(test_dir, exist_ok=True)
    
    #Definicion de archivos para testear 
    test_file = os.path.join(test_dir, 'test_file.txt')
    
    #Creacion del archivo para asociarlo a un Blob
    with open(test_file, 'w') as f:
        f.write('Test')

    yield test_dir, test_file

    # Al finalizar los tests, eliminamos el directorio y todo su contenido
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

@pytest.fixture
def business(setup_and_cleanup):
    test_dir, test_file = setup_and_cleanup

    mock_file = Mock()
    mock_file.save = Mock()

    obj = Business(test_dir)
    blob_id = obj.put_blob('blob_1', 'owner_1', ['admin'], test_file, mock_file)
    yield obj, blob_id
    
def test_create_business(business, setup_and_cleanup):
    obj, blob_id = business
    test_dir, test_file = setup_and_cleanup

    assert obj is not None
    assert obj.persistence is not None
    assert obj.persistence.json_path is not None
    
def test_detele_blob_OK(business):
    obj, blob_id = business
        
    code = obj.delete_blob(blob_id, 'token_for_admin', ['admin'])
    assert code is 200

def test_detele_blob_permission_FAIL(business):
    obj, blob_id = business

    with pytest.raises(Forbidden):
        obj.delete_blob(blob_id, 'token_for_user', ['user'])

def test_detele_blob_exits_FAIL(business):
    obj, blob_id = business

    code = obj.delete_blob('dwqedfqcdas', 'token_for_user', ['user'])
    assert code == 404
    
def test_get_file_blob_OK(business):
    obj, blob_id = business
        
    file, code = obj.get_file_blob(blob_id, 'token_for_admin', ['admin'])
    assert file is not None
    assert code is 200

def test_get_file_blob_permission_FAIL(business):
    obj, blob_id = business

    with pytest.raises(Forbidden):     
        obj.get_file_blob(blob_id, 'token_for_user', ['user'])
   

def test_get_file_blob_exits_FAIL(business):
    obj, blob_id = business
        
    path, code = obj.get_file_blob('edfadawdawdaw', 'token_for_admin', ['admin'])
    assert code == 404


def test_get_name_blob_OK(business):
    obj, blob_id = business
        
    name, code = obj.get_name_blob(blob_id, 'token_for_admin', ['admin'])
    assert name is not None
    assert code is 200

def test_get_name_blob_permission_FAIL(business):
    obj, blob_id = business
        
    with pytest.raises(Forbidden):        
        obj.get_name_blob(blob_id, 'token_for_user', ['user'])
    
def test_get_name_blob_exits_FAIL(business):
    obj, blob_id = business
        
    name, code = obj.get_name_blob('dwdadadaww', 'token_for_admin', ['admin'])
    assert code == 404

def test_get_roles_blob_OK(business):
    obj, blob_id = business
        
    roles, code = obj.get_roles_blob(blob_id, 'token_for_admin', ['admin'])
    assert roles is not None
    assert code is 200

def test_get_roles_blob_permission_FAIL(business):
    obj, blob_id = business
        
    with pytest.raises(Forbidden):  
        obj.get_roles_blob(blob_id, 'token_for_user', ['user'])
   

def test_get_roles_blob_exits_FAIL(business):
    obj, blob_id = business
        
    roles, code = obj.get_roles_blob('dwdadadada', 'token_for_admin', ['admin'])
    assert roles is None
    assert code == 404

def test_modify_file_blob_OK(business, ):
    obj, blob_id = business
        
    # Creamos un objeto FileStorage para simular el archivo
    new_file_path = './test/test_file.txt'
    with open(new_file_path, 'w') as file:
        file.write("Contenido de prueba")

    with open(new_file_path, 'rb') as f:
        new_file = FileStorage(f, filename="test_file.txt")
        
        code = obj.modify_file_blob(blob_id, 'token_for_admin', ['admin'], new_file)
        
        #Eliminamos el archivo que hemos creado para la prueba
        os.remove(new_file_path)
        
        assert code == 200

def test_modify_file_blob_permission_FAIL(business, ):
    obj, blob_id = business
        
    # Creamos un objeto FileStorage para simular el archivo
    new_file_path = './test/test_file.txt'
    with open(new_file_path, 'w') as file:
        file.write("Contenido de prueba")

    with open(new_file_path, 'rb') as f:
        new_file = FileStorage(f, filename="test_file.txt")
        
        with pytest.raises(Forbidden): 
            obj.modify_file_blob(blob_id, 'token_for_user', ['user'], new_file)

        #Eliminamos el archivo que hemos creado para la prueba
        os.remove(new_file_path) 

def test_modify_file_blob_exits_FAIL(business, ):
    obj, blob_id = business
        
    # Creamos un objeto FileStorage para simular el archivo
    new_file_path = './test/test_file.txt'
    with open(new_file_path, 'w') as file:
        file.write("Contenido de prueba")

    with open(new_file_path, 'rb') as f:
        new_file = FileStorage(f, filename="test_file.txt")

        code = obj.modify_file_blob('dwdacwadfae', 'token_for_admin', ['admin'], new_file)

        #Eliminamos el archivo que hemos creado para la prueba
        os.remove(new_file_path)

        assert code == 404

def test_modify_name_blob_OK(business):
    obj, blob_id = business
        
    code = obj.modify_name_blob(blob_id, 'token_for_admin', ['admin'], 'new_name')
    assert code is 200

def test_modify_name_blob_permission_FAIL(business):
    obj, blob_id = business
        
    with pytest.raises(Forbidden):
        obj.modify_name_blob(blob_id, 'token_for_user', ['user'], 'new_name')
    
def test_modify_name_blob_exits_FAIL(business):
    obj, blob_id = business
        
    code = obj.modify_name_blob('dwadasdasdasd', 'token_for_admin', ['admin'], 'new_name')
    assert code == 404

def test_modify_roles_blob_OK(business):
    obj, blob_id = business
        
    code = obj.modify_roles_blob(blob_id, 'token_for_admin', ['admin'], ['new_role'])
    assert code is 200

def test_modify_roles_blob_permission_FAIL(business):
    obj, blob_id = business
    
    with pytest.raises(Forbidden):
        obj.modify_roles_blob(blob_id, 'token_for_user', ['user'], ['new_role'])

def test_modify_roles_blob_exits_FAIL(business):
    obj, blob_id = business
        
    code = obj.modify_roles_blob('dwadasdsad', 'token_for_admin', ['admin'], ['new_role'])
    assert code == 404