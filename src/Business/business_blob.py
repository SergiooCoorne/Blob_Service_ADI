from src.Persistence.persistence_blob import Persistence, BlobNotFound 
#from persistence_blob import Persistence, BlobNotFound #AVERIGUAR PORQUE NO ME DEJA IMPORTAR EL MODULO SI PONGO DE RUTA 'src.Persistence.persistence_blob'
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
        
    def put_blob(self, name: str, owner: str, roles: List[str], data: bytes) -> str:
        blob_id, rtr = self.persistence.create_blob(name, owner, roles, data)
        if rtr is True:
            return blob_id
        
        return None
    
    def delete_blob(self, blob_id: str, authToken: str) -> int:
        permission = False #Valor para verificar si se puede hacer la operacion o no
        roles_user, name_user = get_data_token(authToken) #Obtenemos los roles del usuario
        roles_blob = self.persistence.get_roles_blob(blob_id) #Obtenemos los roles del blob
        
        #Comprobacion de que el user este dentro de algunos de los roles del blob
        for rol_user in roles_user:
            if rol_user in roles_blob:
                permission = True
                break
        
        #Si tiene permisos se hace la operacion
        if permission:
            rtr = self.persistence.delete_blob(blob_id)
            if rtr:
                return 200
            
        else:
            raise Forbidden(blob_id, roles_blob)
        
    def get_data_blob(self, blob_id: str) -> Union[bytes, int]:
        data = self.persistence.get_data_blob(blob_id)
        if data:
            return data, 200
        else:
            return None, 404
        
    def get_name_blob(self, blob_id: str) -> Union[str, int]:    
        name = self.persistence.get_name_blob(blob_id)
        if name:
            return name, 200
        else:
            return None, 404
    
    def get_owner_blob(self, blob_id: str) -> Union[str, int]:
        owner = self.persistence.get_owner_blob(blob_id)
        if owner:
            return owner, 200
        else:
            return None, 404

    def get_roles_blob(self, blob_id: str) -> Union[List[str], int]:
        roles = self.persistence.get_roles_blob(blob_id)
        if roles:
            return roles, 200
        else:
            return None, 404
         
    def modify_data_blob(self, blob_id: str, authToken: str, new_data: bytes) -> int:
        permission = False
        roles_user, name_user = get_data_token(authToken)
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob:
                permission = True
                break
            
        if permission:
            rtr = self.persistence.modify_data_blob(blob_id, new_data)
            
            if rtr:
                return 200
        
        return 404
    
    def modify_name_blob(self, blob_id: str, authToken: str, new_name: str) -> int:
        permission = False
        roles_user, name_user = get_data_token(authToken)
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob:
                permission = True
                break
            
        if permission:
            rtr = self.persistence.modify_name_blob(blob_id, new_name)
            
            if rtr:
                return 200
        
        return 404
    
    def modify_owner_blob(self, blob_id: str, authToken: str, new_owner: str) -> int:
        permission = False
        roles_user, name_user = get_data_token(authToken)
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob:
                permission = True
                break
            
        if permission:
            rtr = self.persistence.modify_owner_blob(blob_id, new_owner)
            
            if rtr:
                return 200
        
        return 404
    
    def modify_roles_blob(self, blob_id: str, authToken: str, new_roles: List[str]) -> int:
        permission = False
        roles_user, name_user = get_data_token(authToken)
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob:
                permission = True
                break
            
        if permission:
            rtr = self.persistence.modify_roles_blob(blob_id, new_roles)
            
            if rtr:
                return 200
        
        return 404
    
def get_data_token(authToken) -> Union[List[str], str]:
    response = requests.get(
        f'{URL_TOKEN_SERVICE}/api/v1/token/{authToken}'
    )
    
    if response.status_code != 200:
        raise Exception(f'Token {authToken} not found')
    
    roles = response.json().get('roles')
    owner = response.json().get('username')
        
    return roles, owner