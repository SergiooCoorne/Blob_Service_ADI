import secrets
import json
import os
from typing import Union

class BlobNotFound(Exception):
    """Excepción para cuando un Blob_ID no se encuentra en el JSON."""
    def __init__(self, blob_id):
        super().__init__(f"Exception: Blob con ID '{blob_id}' no encontrado.")
        self.blob_id = blob_id
        self.status_code = 404

class Blob:
    def __init__(self, name: str, owner: str, roles: list[str], file_path: str):
        self.name = name
        self.owner = owner
        self.blob_id = secrets.token_hex(8)
        self.roles = roles
        self.file_path = file_path
        
    def get_blob_id(self) -> str:
        return self.blob_id
    
    def get_blob_name(self) -> str:
        return self.name
    
    def get_blob_owner(self) -> str:
        return self.owner
    
    def get_path_file_blob(self) -> str:
        return self.file_path
    
    def get_blob_roles(self) -> list:
        return self.roles

class Persistence:
    def __init__(self, persistence_path: str):
        self.path_persistence = persistence_path
        self.json_path = f'{persistence_path}/persistence.json'

        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as f:
                json.dump({}, f)  # Escribimos un objeto JSON vacío
            os.chmod(self.json_path, 0o777)

    def create_blob(self, name: str, owner: str, roles: list[str], file_path: str, file) -> Union[str, bool]:
        rtn = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no
        new_blob = Blob(name, owner, roles, file_path) #Creamos el Blob para tener referencia al archivo que vamos a subir
        
        file.save(file_path) #Subimos del archivo
        
        #Leemos los datos del JSON
        with open(self.json_path, 'r',) as persistence_json:
            data_json = json.load(persistence_json)
    
        # Agreamos ahora el nuevo Blob cuya clave sera su Blob_ID, y de esta manera lo podemos identificar en el JSON
        blob_data = {
            "Blob_Name": new_blob.get_blob_name(),
            "Blob_Owner": new_blob.get_blob_owner(),
            "Blob_Roles": new_blob.get_blob_roles(),
            "Blob_Path_File": file_path
        }
        data_json[new_blob.get_blob_id()] = blob_data

        with open(self.json_path, 'w', encoding='utf-8') as persistence_json:
            json.dump(data_json, persistence_json, indent=4)
            rtn = True

        return new_blob.get_blob_id(), rtn
    
    def modify_file_blob(self, blob_id: str, new_file: str) -> bool:
        rtr = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Primero borramos el archivo asociado al Blob
        if os.path.exists(self.get_path_file_blob(blob_id)):
            os.remove(self.get_path_file_blob(blob_id))
        
        #Ahora sacamos la ruta completa del nuevo file
        filename = os.path.basename(new_file.filename) 
        #Juntamos la ruta de nuestro directorio de persistencia con el nombre del archivo
        file_path = os.path.join(self.path_persistence, filename)
        
        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Path_File"] = file_path
        
        #Volvemos a escribir en el JSON
        with open(self.json_path, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True

        #Por ultimo, guardamos el archivo        
        new_file.save(file_path)
        
        return rtr
    
    def get_path_file_blob(self, blob_id: str) -> str:
        #Leemos los datos del JSON
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        data = data_json[blob_id]['Blob_Path_File']

        return data
    
    def get_name_blob(self, blob_id: str) -> str:
        #Leemos los datos del JSON
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        return data_json[blob_id]['Blob_Name']
    
    def modify_name_blob(self, blob_id: str, new_name: str) -> bool:
        rtr = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Name"] = new_name
    
        #Escribimos del nuevo el JSON
        with open(self.json_path, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True

        return rtr
    
    def get_roles_blob(self, blob_id: str) -> list[str]:
        #Leemos los datos del JSON
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        return data_json[blob_id]['Blob_Roles']
    
    def modify_roles_blob(self, blob_id: str, new_roles: list[str]) -> bool:
        rtr = False
        
        #Leeemos el JSON para obtener los datos que hay en el
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        #Procedemos a modificar lo que se quiere modificar el Blob
        data_json[blob_id]["Blob_Roles"] = new_roles
        
        #Escribimos del nuevo el JSON
        with open(self.json_path, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtr = True
            
        return rtr
    
    def delete_blob(self, blob_id: str) -> Union[int, bool]:
        rtn = False #Valor que se va a devolver para verificar si se ha hecho de forma correcta la operacion o no

        #Leemos los datos del JSON
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)
        
        if data_json[blob_id] == '':
            return 204, False

        #Borramos el blob_ID del JSON
        del data_json[blob_id]
        os.remove(self.get_path_file_blob(blob_id)) #Borramos el archivo del Blob

        #Escribimos del nuevo el JSON
        with open(self.json_path, 'w') as persistence_json:
            json.dump(data_json, persistence_json, indent = 4)
            rtn = True

        return rtn
    
    def blob_exits(self, blob_id):
        #Leemos los datos del JSON
        with open(self.json_path, 'r') as persistence_json:
            data_json = json.load(persistence_json)

        #Comprobamos que el Blob_ID esta dentro del JSON
        if not blob_id in data_json:
            raise BlobNotFound(blob_id)
        else:
            return True