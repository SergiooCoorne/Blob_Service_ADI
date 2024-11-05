from src.Business.business_blob import Business, Forbidden
from src.Persistence.persistence_blob import Blob
import pytest
import os

@pytest.fixture
def business():
    obj = Business()
    blob_id = obj.put_blob('blob_1', 'owner_1', ['admin'], 'file_1')
    yield obj, blob_id
    
def test_create_business(business):
    obj, blob_id = business
    assert obj is not None
    assert obj.persistence is not None
    assert obj.persistence.root_persistence is not None
    assert obj.persistence.root_persistence == './json_test.json'
        
def test_put_blob(business):
    obj, blob_id = business
    blob_id_created = obj.put_blob('blob_1', 'owner_1', ['admin'], 'file_1')
    assert blob_id_created is not None
    
def test_detele_blob_OK(business):
    obj, blob_id = business
        
    code = obj.delete_blob(blob_id, 'token_for_admin', ['admin'])
    assert code is 200
    
def test_get_file_blob_OK(business):
    obj, blob_id = business
        
    file, code = obj.get_file_blob(blob_id, 'token_for_admin', ['admin'])
    assert file is not None
    assert code is 200
    
def test_get_name_blob_OK(business):
    obj, blob_id = business
        
    name, code = obj.get_name_blob(blob_id, 'token_for_admin', ['admin'])
    assert name is not None
    assert code is 200
    
def test_get_owner_blob_OK(business):
    obj, blob_id = business
        
    owner, code = obj.get_owner_blob(blob_id, 'token_for_admin', ['admin'])
    assert owner is not None
    assert code is 200
    
def get_roles_blob_OK(business):
    obj, blob_id = business
        
    roles, code = obj.get_roles_blob(blob_id, 'token_for_admin', ['admin'])
    assert roles is not None
    assert code is 200
    
def test_modify_file_blob_OK(business):
    obj, blob_id = business
        
    code = obj.modify_file_blob(blob_id, 'token_for_admin', ['admin'], 'new_file')
    assert code is 200
    
def test_modify_name_blob_OK(business):
    obj, blob_id = business
        
    code = obj.modify_name_blob(blob_id, 'token_for_admin', ['admin'], 'new_name')
    assert code is 200
    
def test_modify_owner_blob_OK(business):
    obj, blob_id = business
        
    code = obj.modify_owner_blob(blob_id, 'token_for_admin', ['admin'], 'new_owner')
    assert code is 200
    
def test_modify_roles_blob(business):
    obj, blob_id = business
        
    code = obj.modify_roles_blob(blob_id, 'token_for_admin', ['admin'], ['new_role'])
    assert code is 200