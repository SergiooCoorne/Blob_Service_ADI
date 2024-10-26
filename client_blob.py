#!/usr/bin/env python3

from typing import List

import requests

def _assert_status_ok_(status_code):
    if status_code not in [200, 204]:
        raise RuntimeError('Unknown response from API')
    
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
        print(f'Status Code: {response.status_code}')
    
if __name__ == '__main__':
    client = Client('http://localhost:1234/api/v1')
    writted_by = ['Luis', 'Paco', 'Antonio']
    client.put_blob('1234', 'Sergio', writted_by, b'1234')