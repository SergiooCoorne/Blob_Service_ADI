import secrets
import json
import base64
import os
from typing import Union

class BlobNotFound(Exception):
    """Excepción para cuando un Blob_ID no se encuentra en el JSON."""
    def __init__(self, blob_id):
        super().__init__(f"Blob con ID '{blob_id}' no encontrado.")
        self.blob_id = blob_id

class Blob:
    def __init__(self, name: str, owner: str, roles: list[str], file: str):
        self.name = name
        self.owner = owner
        self.blob_id = secrets.token_hex(8)
        self.roles = roles
        self.file = file
        
    def get_blob_id(self) -> str:
        return self.blob_id
    
    def get_blob_name(self) -> str:
        return self.name
    
    def get_blob_owner(self) -> str:
        return self.owner
    
    def get_blob_file(self) -> str:
        return self.file
    
    def get_blob_roles(self) -> list:
        return self.roles

class Persistence:
    def __init__(self):
        self.root_persistence = './json_test.json'
        if not os.path.exists(self.root_persistence):
            with open(self.root_persistence, 'w') as f:
                json.dump({}, f)  # Escribir un objeto JSON vacío

    def create_blob(self, name: str, owner: str, roles: list[str], file: str) -> Union[str, bool]:
        rtn = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no
        new_blob = Blob(name, owner, roles, file)
        #data_encoded = base64.b64encode(new_blob.get_blob_data()).decode('utf-8')
    
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r',) as persistence_json:
            data_json = json.load(persistence_json)
    
        # Agreamos ahora el nuevo Blob cuya clave sera su Blob_ID, y de esta manera lo podemos identificar en el JSON
        blob_data = {
            "Blob_Name": new_blob.get_blob_name(),
            "Blob_Owner": new_blob.get_blob_owner(),
            "Blob_Roles": new_blob.get_blob_roles(),
            "Blob_File": file
        }
        data_json[new_blob.get_blob_id()] = blob_data

        with open(self.root_persistence, 'w', encoding='utf-8') as persistence_json:
            json.dump(data_json, persistence_json, indent=4)
            rtn = True

        return new_blob.get_blob_id(), rtn

    def get_file_blob(self, blob_id: str) -> bytes:
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        #Comprobamos que el Blob_ID que nos estan pasando esta dentro del archivo JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        data = data_json[blob_id]['Blob_File']
        #print(f'Data del blob ID: {blob_id}: {data}')

        return data
    
    def get_name_blob(self, blob_id: str) -> str:
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        #Comprobamos que el Blob_ID que nos estan pasando esta dentro del archivo JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        return data_json[blob_id]['Blob_Name']
    
    def get_owner_blob(self, blob_id: str) -> str:
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        #Comprobamos que el Blob_ID que nos estan pasando esta dentro del archivo JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        return data_json[blob_id]['Blob_Owner']
    
    def get_roles_blob(self, blob_id: str) -> list[str]:
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        #Comprobamos que el Blob_ID que nos estan pasando esta dentro del archivo JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        return data_json[blob_id]['Blob_Roles']
    
    def delete_blob(self, blob_id: str) -> bool:
        rtn = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Leemos los datos del JSON
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        #Borramos el blob_ID del JSON
        del data_json[blob_id]

        #Escribimos del nuevo el JSON
        with open(self.root_persistence, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtn = True

        return rtn
    
    def modify_file_blob(self, blob_id: str, new_file: str) -> bool:
        rtr = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        #Procedemos a modificar lo que se quiere modificar el Blob
        #new_data_encoded = base64.b64encode(new_data).decode('utf-8')
        data_json[blob_id]["Blob_File"] = new_file
    
        #Escribimos del nuevo el JSON
        with open(self.root_persistence, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True

        return rtr
    
    def modify_name_blob(self, blob_id: str, new_name: str) -> bool:
        rtr = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Name"] = new_name
    
        #Escribimos del nuevo el JSON
        with open(self.root_persistence, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True

        return rtr
    
    def modify_owner_blob(self, blob_id: str, new_owner: str) -> bool:
        rtr = False
        
        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
            
        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Owner"] = new_owner
        
        #Escribimos del nuevo el JSON
        with open(self.root_persistence, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True
            
        return rtr
    
    def modify_roles_blob(self, blob_id: str, new_roles: list[str]) -> bool:
        rtr = False
        
        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
            
        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Roles"] = new_roles
        
        #Escribimos del nuevo el JSON
        with open(self.root_persistence, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True
            
        return rtr