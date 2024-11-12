import pytest
from requests_toolbelt import MultipartEncoder
import os

@pytest.fixture
def blob_for_test(client):
    client = client

    #Creamos un archivo de prueba para subirlo
    with open('./test_file.txt', 'w') as file:
        file.write('TEST')

    with open('./test_file2.txt', 'w') as file:
        file.write('TEST2')

    with open('./test_file.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'name': 'blob_1',
                'writable_by': 'paco',
                'owner': 'sergio',
                'file': ('./test_file.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.put(
            '/api/v1/blob',
            headers = {
                'AuthToken': '12334',
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
        blob_id_1 = response.text.split(': ')[1]

    with open('./test_file2.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'name': 'blob_1',
                'writable_by': 'paco',
                'owner': 'sergio',
                'file': ('./test_file2.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.put(
            '/api/v1/blob',
            headers = {
                'AuthToken': '12334',
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
        blob_id_2 = response.text.split(': ')[1] 

    yield blob_id_1, blob_id_2
    os.remove('./test_file.txt')
    os.remove('./test_file2.txt')

def test_put_blob(client):
    #Creamos un archivo de prueba para subirlo
    with open('./test_file.txt', 'w') as file:
        file.write('TEST')

    with open('./test_file.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'name': 'blob_1',
                'writable_by': 'paco',
                'owner': 'sergio',
                'file': ('./test_file.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.put(
            '/api/v1/blob',
            headers = {
                'AuthToken': '12334',
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
    #Eliminamos el archivo de prueba
    os.remove('./test_file.txt')

    assert response.status_code == 201

def test_put_blob_without_token(client):
     #Creamos un archivo de prueba para subirlo
    with open('./test_file.txt', 'w') as file:
        file.write('TEST')

    with open('./test_file.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'name': 'blob_1',
                'writable_by': 'paco',
                'owner': 'sergio',
                'file': ('./test_file.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.put(
            '/api/v1/blob',
            headers = {
                'Content-Type': multipart.content_type
            },
            data = multipart
        )    
     #Eliminamos el archivo de prueba
    os.remove('./test_file.txt')

    assert response.status_code == 401

def test_put_blob_without_file(client):
    response = client.put(
        '/api/v1/blob',
        headers = {
            'AuthToken': '12334',
        },
        data = None
    )
    assert response.status_code == 400

def test_delete_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.delete(
        f'/api/v1/blob/{blob_id_1}',
        headers = {
            'AuthToken': 'token_for_admin',
        }
    )
    assert response.status_code == 200

def test_delete_blob_without_token(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.delete(
        f'/api/v1/blob/{blob_id_2}',
        headers = {
        }
    )
    assert response.status_code == 401

def test_delete_blob_not_exits(client):
    response = client.delete(
        '/api/v1/blob/4654534864',
        headers = {
            'AuthToken': 'token_for_admin',
        }
    )
    assert response.text == 'Blob not found'
    assert response.status_code == 404

def test_get_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.get(
        f'/api/v1/blob/{blob_id_2}/data',
        headers = {
            'AuthToken': 'token_for_admin',
        }
    )
    assert response.text != None
    assert response.status_code == 200

def test_get_blob_without_token(client):
    response = client.get(
        '/api/v1/blob/05d11945e8529df7/data',
        headers = {
        }
    )
    assert response.status_code == 401

def test_get_blob_not_exits(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.get(
        f'/api/v1/blob/212372189/data',
        headers = {
            'AuthToken': 'token_for_admin',
        }
    )
    assert response.text == 'Blob not found'
    assert response.status_code == 404

def test_post_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    #Creamos un archivo de prueba para subirlo
    with open('./test_file3.txt', 'w') as file:
        file.write('TEST')

    with open('./test_file3.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'file': ('./test_file3.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.post(
            f'/api/v1/blob/{blob_id_2}/data',
            headers = {
                'AuthToken': 'token_for_admin',
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
    #Eliminamos el archivo de prueba
    os.remove('./test_file3.txt')
    assert response.status_code == 200

def test_post_blob_without_token(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    #Creamos un archivo de prueba para subirlo
    with open('./test_file3.txt', 'w') as file:
        file.write('TEST')

    with open('./test_file3.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'file': ('./test_file3.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.post(
            f'/api/v1/blob/{blob_id_2}/data',
            headers = {
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
    #Eliminamos el archivo de prueba
    os.remove('./test_file3.txt')
    assert response.status_code == 401

def test_post_blob_not_exits(client):
    #Creamos un archivo de prueba para subirlo
    with open('./test_file3.txt', 'w') as file:
        file.write('TEST')

    with open('./test_file3.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'file': ('./test_file3.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.post(
            f'/api/v1/blob/6321798/data',
            headers = {
                'AuthToken': 'token_for_admin',
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
    #Eliminamos el archivo de prueba
    os.remove('./test_file3.txt')
    assert response.text == 'Blob not found'
    assert response.status_code == 404

def test_get_roles_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.get(
        f'/api/v1/blob/{blob_id_2}/roles',
        headers = {
            'AuthToken': 'token_for_admin'
        },
    )
    assert response.text != None
    assert response.status_code == 200

def test_get_roles_blob_without_token(client):
    response = client.get(
        '/api/v1/blob/05d11945e8529df7/roles',
        headers = {
        },
    )
    assert response.status_code == 401

def test_get_roles_blob_not_exits(client):
    response = client.get(
        f'/api/v1/blob/687687572/roles',
        headers = {
            'AuthToken': 'token_for_admin'
        },
    )
    assert response.text == 'Blob not found'
    assert response.status_code == 404

def test_post_roles_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.post(
        f'/api/v1/blob/{blob_id_2}/roles',
        headers = {
            'AuthToken': 'token_for_admin'
        },
        json = {
                    'writable_by': ['jesus', 'fran', 'jaime']
                }
    )
    assert response.status_code == 200

def test_post_roles_blob_without_token(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.post(
        f'/api/v1/blob/{blob_id_2}/roles',
        headers = {},
        json = {
                    'writable_by': ['jesus', 'fran', 'jaime']
                }
    )
    assert response.status_code == 401

def test_post_roles_blob_not_exits(client):
    response = client.post(
        f'/api/v1/blob/6432473280/roles',
        headers = {
            'AuthToken': 'token_for_admin'
        },
        json = {
                    'writable_by': ['jesus', 'fran', 'jaime']
                }
    )
    assert response.text == 'Blob not found'
    assert response.status_code == 404

def test_get_name_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.get(
        f'/api/v1/blob/{blob_id_2}/name',
        headers = {
            'AuthToken': 'token_for_admin'
        },
    ) 
    assert response.text != None
    assert response.status_code == 200

def test_get_name_blob_without_token(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.get(
        f'/api/v1/blob/{blob_id_2}/name',
        headers = {
        },
    )
    assert response.status_code == 401

def test_get_name_blob_not_exits(client):
    response = client.get(
        f'/api/v1/blob/4738247329/name',
        headers = {
            'AuthToken': 'token_for_admin'
        },
    ) 
    assert response.text == 'Blob not found'
    assert response.status_code == 404

def test_post_name_blob(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.post(
        f'/api/v1/blob/{blob_id_2}/name',
        headers = {
            'AuthToken': 'token_for_admin'
        },
        json = {
                    'name': 'test_name'
        }
    )
    assert response.status_code == 200

def test_post_name_blob_without_token(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.post(
        f'/api/v1/blob/{blob_id_2}/name',
        headers = {},
        json = {
                    'name': 'test_name'
        }
    )
    assert response.status_code == 401

def test_post_name_blob_not_exits(client, blob_for_test):
    blob_id_1, blob_id_2 = blob_for_test

    response = client.post(
        f'/api/v1/blob/4732564289/name',
        headers = {
            'AuthToken': 'token_for_admin'
        },
        json = {
                    'name': 'test_name'
        }
    )
    assert response.text == 'Blob not found'
    assert response.status_code == 404