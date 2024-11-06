from typing import List
import requests
from requests_toolbelt import MultipartEncoder

def _assert_status_ok_(status_code):
    if status_code not in [200, 201, 204, 400, 401, 404]:
        raise RuntimeError('Unknown response from API')
    else:
        return True
    
class Client:
    def __init__(self, root_api: str) -> None:
        self.root_api = root_api
        
    def put_blob(self, auth_token: str, name: str, writer: List[str], file_path: str) -> None:
        with open(file_path, 'rb') as file:
            multipart = MultipartEncoder(
                fields={
                    'name': name,
                    'writable_by': ', '.join(writer),
                    'owner': writer[0],
                    'file': (file_path, file, 'application/octet-stream')
                }
            )

            response = requests.put(
                f'{self.root_api}/blob',
                headers={
                    'AuthToken': auth_token,
                    'Content-Type': multipart.content_type
                },
                data = multipart
            )

        _assert_status_ok_(response.status_code)
        print(f'Status Code Put_Data Request: {response.status_code}')
    
    def delete_blob(self, blob_id: str) -> None:
        response = requests.delete(
            f'{self.root_api}/blob/{blob_id}',
            headers = {'AuthToken': 'token_for_admin'}
        )
        if _assert_status_ok_(response.status_code):
            print(f'Status Code Delete_Data Request: {response.status_code}')
    
    def get_blob(self, blob_id: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/data',
            headers = {'AuthToken': 'token_for_admin'}
        )
        _assert_status_ok_(response.status_code)
        print(f'Status Code Get_Data Request: {response.status_code}')
        file = response.content
        
        print(f'File: {file}')    

    def post_patch_blob(self, blob_id: str, auth_token: str, file_path: str, request: str) -> None:
        if request == 'POST':
            with open(file_path, 'rb') as file:
                multipart = MultipartEncoder(
                    fields={
                        'file': (file_path, file, 'application/octet-stream')
                    }
                )
            
                response = requests.post(
                    f'{self.root_api}/blob/{blob_id}/data',
                    headers={
                        'AuthToken': auth_token,
                        'Content-Type': multipart.content_type
                    },
                    data = multipart
                )

            _assert_status_ok_(response.status_code)
            print(f'Status Code POST_Data Request: {response.status_code}')
        
        elif request == 'PATCH':
            with open(file_path, 'rb') as file:
                multipart = MultipartEncoder(
                    fields={
                        'file': (file_path, file, 'application/octet-stream')
                    }
                )
            
                response = requests.patch(
                    f'{self.root_api}/blob/{blob_id}/data',
                    headers={
                        'AuthToken': auth_token,
                        'Content-Type': multipart.content_type
                    },
                    data = multipart
                )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Patch_Data Request: {response.status_code}')
            
        else:
            raise ValueError('Unknown request')
    
    def get_roles_blob(self, blob_id: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/roles',
            headers = {'AuthToken': 'token_for_admin'},)
        
        _assert_status_ok_(response.status_code)
        print(f'{response.status_code}, data: {response.json()}')
        roles = response.json()

    def post_patch_roles_blob(self, blob_id: str, new_roles: List[str], request: str) -> None:
        if request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/{blob_id}/roles',
                headers = {'AuthToken': 'token_for_admin'},
                json = {
                    'writable_by': new_roles
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Patch_Name Request: {response.status_code}')

        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/{blob_id}/roles',
                headers = {'AuthToken': 'token_for_admin'},
                json = {
                    'writable_by': new_roles
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'Status Code Post_Name Request: {response.status_code}')

    def get_name_blob(self, blob_id: str) -> None:
        response = requests.get(
            f'{self.root_api}/blob/{blob_id}/name',
            headers = {'AuthToken': 'token_for_admin'},)
        _assert_status_ok_(response.status_code)
        name = response.text
        print(f'{response.status_code}. Name: {name}')

    def post_patch_names_blob(self, blob_id: str, name: str, request: str) -> None:
        if request == 'PATCH':
            response = requests.patch(
                f'{self.root_api}/blob/{blob_id}/name',
                headers = {'AuthToken': 'token_for_admin'},
                json = {
                    'name': name
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'{response.status_code}.{response.text}')

        if request == 'POST':
            response = requests.post(
                f'{self.root_api}/blob/{blob_id}/name',
                headers = {'AuthToken': 'token_for_admin'},
                json = {
                    'name': name
                }
            )
            _assert_status_ok_(response.status_code)
            print(f'{response.status_code}.{response.text})')
    

if __name__ == '__main__':
    client = Client('http://localhost:1234/api/v1')
    #writted_by = ['admin', 'Paco', 'Antonio']
    #blob_id = client.put_blob('token_for_admin', 'blob_1', writted_by, '/home/sergio/Escritorio/prueba.txt')
    # client.delete_blob('2e93083dbde9f18a')
    #client.get_blob('38f1ad88e7f84c80')
    client.post_patch_blob('06db2bec3c10c78', 'token_for_admin', '/home/sergio/Escritorio/prueba2.txt', 'POST')
    #client.post_patch_blob('38f1ad88e7f84c80', 'token_for_admin', '/home/sergio/Escritorio/prueba.txt', 'PATCH')
    #client.get_roles_blob('38f1ad88e7f84c80')
    #client.post_patch_roles_blob('06db2be4c3c10c78', ['jesus', 'fran', 'jaime'], 'POST')
    #client.post_patch_roles_blob('06db2be4c3c10c78', ['paco', 'admin', 'antonio'], 'PATCH')
    #client.get_name_blob('06db2be4c3c10c78')
    #client.post_patch_names_blob('06db2be4c3c10c78', 'blob_2', 'POST')