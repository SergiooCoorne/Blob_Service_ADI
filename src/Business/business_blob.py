import sys
sys.path.append("/home/sergio/Escritorio/Uni/Primer_Cutri/ADI/Trabajo_1_ADI")

from src.Persistence.persistence_blob import Persistence, BlobNotFound 
from typing import List, Union
import requests
from requests_toolbelt import MultipartEncoder

class Forbidden(Exception):
    """Excepción para cuando un Blob_ID no se encuentra en el JSON."""
    def __init__(self, blob_id, roles):
        super().__init__(f"{blob_id}, {roles}")
        self.blob_id = blob_id

class Business:
    def __init__(self):
        self.persistence = Persistence()
        
    def put_blob(self, name: str, owner: str, roles: List[str], file_path: str, file) -> str:
        blob_id, rtr = self.persistence.create_blob(name, owner, roles, file_path, file)
        if rtr is True:
            return blob_id
        
        return None
        
    def delete_blob(self, blob_id: str, authToken: str, roles_user: List[str]) -> int:
        permission = False #Valor para verificar si se puede hacer la operacion o no
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id) #Obtenemos los roles del blob
        
        #Comprobacion de que el user este dentro de algunos de los roles del blob
        for rol_user in roles_user:
            if rol_user in roles_blob or rol_user == 'admin':
                permission = True
                break
        
        #Si tiene permisos se hace la operacion
        if permission:
            rtr = self.persistence.delete_blob(blob_id)
            if rtr:
                return 200
        else:
            return 401
            #raise Forbidden(blob_id, roles_blob)
        
    def get_file_blob(self, blob_id: str, authToken: str, roles_user: List[str]) -> Union[str, int]:
        permission = False
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob or rol_user == 'admin':
                permission = True
                break
                
        if permission:
            return self.persistence.get_path_file_blob(blob_id), 200
        else:
            return None, 401 
        
    def get_name_blob(self, blob_id: str, authToken: str, roles_user: List[str]) -> Union[str, int]:    
        permission = False
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob or role_user == 'admin':
                permission = True
                break
        
        if permission:
            return self.persistence.get_name_blob(blob_id), 200
        else:
            return None, 401 
    
    def get_roles_blob(self, blob_id: str, authToken: str, roles_user: List[str]) -> Union[List[str], int]:
        permission = False
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id)        
        for role_user in roles_user:
            if role_user in roles_blob or rol_user == 'admin':
                permission = True
                break
        
        if permission:
            return roles_blob, 200
        else:
            return None, 401 
        
    def modify_file_blob(self, blob_id: str, authToken: str, roles_user: List[str], new_file: str) -> int:
        permission = False
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob or rol_user == 'admin':
                permission = True
                break
            
        if permission:
            try:   
                rtr = self.persistence.modify_file_blob(blob_id, new_file)
                if rtr:
                    return 200
            except BlobNotFound:
                return 404
            
        return 401
    
    def modify_name_blob(self, blob_id: str, authToken: str, roles_user: List[str], new_name: str) -> int:
        permission = False
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob or role_user == 'admin':
                permission = True
                break
            
        if permission:
            rtr = self.persistence.modify_name_blob(blob_id, new_name)
            
            if rtr:
                return 200
        
    def modify_roles_blob(self, blob_id: str, authToken: str, roles_user: List[str], new_roles: List[str]) -> int:
        permission = False
        
        try:
            exits = self.persistence.blob_exits(blob_id)    
        except Exception as e:
            print(str(e))
            return e.status_code
        
        roles_blob = self.persistence.get_roles_blob(blob_id)
        
        for role_user in roles_user:
            if role_user in roles_blob or role_user == 'admin':
                permission = True
                break
            
        if permission:
            rtr = self.persistence.modify_roles_blob(blob_id, new_roles)
            
            if rtr:
                return 200
        
        return 404
    
# if __name__ == '__main__':
    # obj = Business()
    # obj.put_blob('name_1', 'owner_yo', ['rol_1', 'rol_2'], 'path')