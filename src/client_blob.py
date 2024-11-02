#!/usr/bin/env python3

from typing import List
import requests

def _assert_status_ok_(status_code):
    if status_code not in [200, 201, 204, 400, 401]:
        raise RuntimeError('Unknown response from API')
    else:
        return True
    
class Client:
    def __init__(self, root_api: str) -> None:
        self.root_api = root_api
        
    def put_blob(self, auth_token: str, name: str, writer: List[str], data: str) -> None:
        response = requests.put(
            f'{self.root_api}/blob',
            headers = {'AuthToken': auth_token},
            json = {
                'name': name,
                'writable_by': writer,
                'multipart': data
            }
        )
        _assert_status_ok_(response.status_code)
        print(f'Status Code Put_Data Request: {response.status_code}')
    
    def delet_blob(self, blob_id: str) -> None:
        response = requests.delete(
            f'{self.root_api}/blob/{blob_id}',
            headers = {'AuthToken': '1234'}
        )
        if _assert_status_ok_(response.status_code):
            print(f'Status Code Delete_Data Request: {response.status_code}')
    
    def get_blob(self, blob_id: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/data',
            headers = {'AuthToken': '1234'}
        )
        _assert_status_ok_(response.status_code)
        print(f'Status Code Get_Data Request: {response.status_code}')    

    def post_patch_blob(self, blob_id: str, data: str, request: str) -> None:
        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/{blob_id}/data',
                headers = {'AuthToken': '1234'},
                json = {
                    'multipart': data
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Post_Data Request: {response.status_code}')
        
        elif request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/{blob_id}/data',
                headers = {'AuthToken': '1234'},
                json = {
                    'multipart': data
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Patch_Data Request: {response.status_code}')
            
        else:
            raise ValueError('Unknown request')
    
    def get_roles_blob(self, blob_id: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/roles',
            headers = {'AuthToken': '1234'},)
        
        _assert_status_ok_(response.status_code)
        print(f'Status Code GET_Roles Request: {response.status_code}')

    def post_patch_roles_blob(self, blob_id: str, roles: list, request: str) -> None:
        if request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/<blob_id>/roles',
                headers = {'AuthToken': '12345'},
                json = {
                    'writable_by': roles
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code: {response.status_code}')

        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/<blob_id>/roles',
                headers = {'AuthToken': '12345'},
                json = {
                    'writable_by': roles
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Post_Patch_Roles Request: {response.status_code}')

    def get_name_blob(self, blob_id: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/name',
            headers = {'AuthToken': '1234'},)
        _assert_status_ok_(response.status_code)
        print(f'Status Code Get_Name Request: {response.status_code}')

    def post_patch_roles_blob(self, blob_id: str, name: str, request: str) -> None:
        if request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/<blob_id>/name',
                headers = {'AuthToken': '12345'},
                json = {
                    'name': name
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Patch_Name Request: {response.status_code}')

        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/<blob_id>/roles',
                headers = {'AuthToken': '12345'},
                json = {
                    'name': name
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Post_Name Request: {response.status_code}')

if __name__ == '__main__':
    client = Client('http://localhost:1234/api/v1')
    writted_by = ['Luis', 'Paco', 'Antonio']
    client.put_blob('1234', 'Sergio', writted_by, '1234')
    client.delet_blob('1234567889')
    client.get_blob('1234567889')
    client.post_patch_blob('1234567889', '1234', 'POST')
    client.post_patch_blob('4564651534', '5678', 'PATCH')
    client.get_roles_blob('12345678')
    client.post_patch_roles_blob('1345756', ['paco', 'sergio', 'alejandro'], 'POST')
    client.post_patch_roles_blob('1345756', ['paco', 'sergio', 'alejandro'], 'PATCH')