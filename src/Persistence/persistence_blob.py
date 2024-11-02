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
    def __init__(self, name: str, roles: list[str], data: bytes):
        self.name = name
        self.blob_id = secrets.token_hex(8)
        self.roles = roles
        self.data = data
    
    def get_blob_id(self) -> str:
        return self.blob_id
    
    def get_blob_name(self) -> str:
        return self.name
    
    def get_blob_data(self) -> bytes:
        return self.data
    
    def get_blob_roles(self) -> list:
        return self.roles

class Persistence:
    def __init__(self, root_persistence: str):
        self.root_persistence = root_persistence
        if not os.path.exists(self.root_persistence):
            with open(self.root_persistence, 'w') as f:
                json.dump({}, f)  # Escribir un objeto JSON vacío

    def create_blob(self, name: str, roles: list[str], data: bytes) -> Union[str, bool]:
        rtn = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no
        new_blob = Blob(name, roles, data)
        data_encoded = base64.b64encode(new_blob.get_blob_data()).decode('utf-8')
    
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r',) as persistence_json:
            data_json = json.load(persistence_json)
    
        # Agreamos ahora el nuevo Blob cuya clave sera su Blob_ID, y de esta manera lo podemos identificar en el JSON
        blob_data = {
            "Blob_Name": new_blob.get_blob_name(),
            "Blob_Roles": new_blob.get_blob_roles(),
            "Blob_Data": data_encoded
        }
        data_json[new_blob.get_blob_id()] = blob_data

       
        with open(self.root_persistence, 'w', encoding='utf-8') as persistence_json:
            json.dump(data_json, persistence_json, indent=4)
            rtn = True

        return new_blob.get_blob_id(), rtn

    def get_blob_data(self, blob_id: str) -> bytes:
        #Leemos los datos del JSON
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        #Comprobamos que el Blob_ID que nos estan pasando esta dentro del archivo JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        data = base64.b64decode(data_json[blob_id]['Blob_Data'])
        #print(f'Data del blob ID: {blob_id}: {data}')

        return data
    
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
    
    def modify_blob(self, blob_id: str, new_name: str, new_roles: list[str], new_data: bytes) -> bool:
        rtr = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.root_persistence, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        
        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Name"] = new_name
        data_json[blob_id]["Blob_Roles"] = new_roles
        data_json[blob_id]["Blob_Data"] = base64.b64encode(new_data).decode('utf-8')

        #Escribimos del nuevo el JSON
        with open(self.root_persistence, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True

        return rtr

# if __name__ == '__main__':
#     persistencia = Persistence('./persistence.json')
#     blob_id_1 = persistencia.create_blob('Blob_1', ['admin', 'user'], data = 'Hola'.encode())
#     blob_id_2 = persistencia.create_blob('Blob_2', ['admin', 'user'], data = 'Adios'.encode())
#     print(persistencia.get_blob_data(blob_id_1))
#     persistencia.delete_blob(blob_id_2)
#     persistencia.modify_blob(blob_id_1, 'Blob_1_1', ['admin_1', 'user_2'], new_data = 'Adios'.encode())
#     print(persistencia.get_blob_data(blob_id_1))

