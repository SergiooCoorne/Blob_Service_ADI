import pytest
import json
from unittest.mock import patch, MagicMock
from io import BytesIO
from flask import Flask
from src.Presentation.presentation_blob import app
from requests_toolbelt import MultipartEncoder

@pytest.fixture
def client():
    # Crea un cliente de prueba para hacer peticiones a la API
    with app.test_client() as client:
        yield client

def test_put_blob(client):
    with open('/home/sergio/Escritorio/prueba.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'name': 'blob_1',
                'writable_by': 'paco',
                'owner': 'sergio',
                'file': ('/home/sergio/Escritorio/prueba.txt', file, 'application/octet-stream')
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
        
    assert response.status_code == 201

def test_put_blob_without_token(client):
    with open('/home/sergio/Escritorio/prueba.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'name': 'blob_1',
                'writable_by': 'paco',
                'owner': 'sergio',
                'file': ('/home/sergio/Escritorio/prueba.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.put(
            '/api/v1/blob',
            headers = {
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
        
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

#PARA ESTOS TEST ES NECESARIO QUE HAY UN BLOB CON EL ID QUE SE PONE EN EL TEST#
# def test_delete_blob(client):
#     response = client.delete(
#         '/api/v1/blob/4188e9269d805e7f',
#         headers = {
#             'AuthToken': 'token_for_admin',
#         }
#     )
#     assert response.status_code == 200

# def test_delet_blob_without_token(client):
#     response = client.delete(
#         '/api/v1/blob/4188e9269d805e7f',
#         headers = {
#         }
#     )
#     assert response.status_code == 401

def test_delete_blob(client):
    response = client.delete(
        '/api/v1/blob/4654534864',
        headers = {
            'AuthToken': 'token_for_admin',
        }
    )
    assert response.status_code == 404

def test_get_blob(client):
    response = client.get(
        '/api/v1/blob/05d11945e8529df7/data',
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

def test_post_blob(client):
    with open('/home/sergio/Escritorio/prueba2.txt', 'rb') as file:
        multipart = MultipartEncoder(
            fields={
                'file': ('/home/sergio/Escritorio/prueba2.txt', file, 'application/octet-stream')
            }
        )
    
        response = client.post(
            '/api/v1/blob/05d11945e8529df7/data',
            headers = {
                'AuthToken': 'token_for_admin',
                'Content-Type': multipart.content_type
            },
            data = multipart
        )
    assert response.status_code == 200

def test_get_roles_blob(client):
    response = client.get(
        '/api/v1/blob/05d11945e8529df7/roles',
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

def test_post_roles_blob(client):
    response = client.post(
        '/api/v1/blob/05d11945e8529df7/roles',
        headers = {
            'AuthToken': 'token_for_admin'
        },
        json = {
                    'writable_by': ['jesus', 'fran', 'jaime']
                }
    )
    assert response.status_code == 200