from persistence_blob import Persistence #AVERIGUAR PORQUE NO ME DEJA IMPORTAR EL MODULO SI PONGO DE RUTA 'src.Persistence.persistence_blob'
from typing import List, Union
import requests
import time

URL_TOKEN_SERVICE = 'http://127.0.0.1:3002'

class Forbidden(Exception):
    """Excepción para cuando un Blob_ID no se encuentra en el JSON."""
    def __init__(self, blob_id):
        super().__init__(f"{blob_id}, {roles}")
        self.blob_id = blob_id

class Business:
    def __init__(self):
        self.persistence = Persistence()
        
    def put_blob(self, name: str, roles: List[str], data: bytes) -> str:
        blob_id, rtr = self.persistence.create_blob(name, roles, data)
        if rtr is True:
            print(f'Business Layer: Blob creado con exito con id: {blob_id}')
            return blob_id
        else:
            print(f'Business Layer: Error al crear el Blob')    
        
    def delete_blob(self, blob_id: str, authToken: str) -> None:
        permission = False #Valor para verificar si se puede hacer la operacion o no
        roles_user, name_user = get_data_token(authToken) #Obtenemos los roles del usuario
        roles_blob = self.persistence.get_blob_roles(blob_id) #Obtenemos los roles del blob
        
        #Comprobacion de que el user este dentro de algunos de los roles del blob
        for rol_user in roles_user:
            if rol_user in roles_blob:
                permission = True
                break
        
        #Si tiene permisos se hace la operacion
        if permission:
            rtr = self.persistence.delete_blob(blob_id)
            print(f'Business Layer: Blob eliminado con exito con id: {blob_id}')
        #Si no, se lanza la excepcion
        else:
            raise Forbidden(blob_id, roles_blob)
        
    
    def get_data_blob(self, blob_id: str) -> bytes:
        pass
        
    def get_roles_blob(self, blob_id: str) -> List[str]:
        pass
        
    def get_name_blob(self, blob_id: str) -> str:    
        pass
        
    def modify_data_blob(self, blob_id: str, authToken: str, roles: List[str], new_data: bytes) -> None:
        pass
        
    def modify_roles_blob(self, blob_id: str, authToken: str, roles: List[str], new_roles: List[str]) -> None:
        pass       
    
    def modify_name_blob(self, blob_id: str, authToken: str, roles: List[str], new_name: str) -> None:
        pass
    

def get_data_token(authToken) -> Union[List[str], str]:
    response = requests.get(
        f'{URL_TOKEN_SERVICE}/api/v1/token/{authToken}'
    )
    
    if response.status_code != 200:
        raise Exception(f'Token {authToken} not found')
    
    roles = response.json().get('roles')
    owner = response.json().get('username')
    
    # print(f'Roles: {roles}')
    # print(f'Owner: {owner}')
    
    return roles, owner
    
# if __name__ == '__main__':
    # business = Business()
    # blod_id = business.put_blob('blob_1', ['admin'], 'data_1'.encode())
    # time.sleep(3)
    # business.delete_blob(blod_id, 'token_for_admin', ['admin'])
    # #get_data_token('token_for_admin')