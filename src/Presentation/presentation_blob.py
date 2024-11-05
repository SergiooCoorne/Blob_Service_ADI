import sys
import os
sys.path.append("/home/sergio/Escritorio/VSCodeLinux/ADI/Trabajo_1_ADI") #Linea necesario para que el interprete de python coja bien las rutas a la hora de lanzar la aplicacion
import argparse
from flask import Flask, Response, request
from typing import List, Union
from src.Business.business_blob import Business
from requests_toolbelt import MultipartEncoder
import getpass
import requests
import json

name_system = getpass.getuser()
URL_TOKEN_SERVICE = 'http://127.0.0.1:3002'

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type = int, required = True, help = "Numero de puerto")
parser.add_argument('-l', '--listening', type = str, required = True, help = "Direccion donde se producirá la escucha")

args = parser.parse_args()

ROOT_API = '/api/v1'
UPLOAD_DIRECTORY = f'/home/{name_system}/persistence_dir'
business = Business()

@app.route(f'{ROOT_API}/blob', methods=('PUT',))
def put_blob():
    auth_token = request.headers.get('AuthToken')
    
    # Comprobación del token
    if not auth_token:
        return Response('Unauthorized', status=401)
    
    # Comprobación del archivo en la petición
    if 'file' not in request.files:
        return Response('Bad Request: No file part', status=400)
    
    #Sacamos el file de la peticion
    file = request.files['file']
    
    #Sacamos el nombre del archivo
    filename = os.path.basename(file.filename) 
    #Juntamos la ruta de nuestro directorio de persistencia con el nombre del archivo
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        
    #Ahora hacemos la parte de la creacion del Blob para tener la referencia al archivo subido y le pasamos el archivo a la capa de negocio
    name = request.form.get('name')
    roles = request.form.get('writable_by')
    owner = request.form.get('owner')
    
    blob_id = business.put_blob(name, owner, roles, file_path, file)

    return Response(f'blob_id: {blob_id}', status=201)

'''Recurso de la API correspondiente con "API_ROOT/blob/{blob_id}" '''
@app.route(f'{ROOT_API}/blob/<blob_id>', methods = ('DELETE',))
def delete_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('Unauthorized', status = 401)

    #Obtenemos los roles del usuario
    roles_user, name_user = get_data_token(auth_token)
    
    #Llamamos a la capa de negocio para que intente hacer la operacion de borrado
    rtr = business.delete_blob(blob_id, auth_token, roles_user)
    
    if rtr == 200:
        return Response(f'Deleted {blob_id}', status = 200)    
    else :
        return Response(f'Unauthorized {blob_id}', status = 401)
    
'''Recurso de la API correspondiente con "API_ROOT/blob/{blob_id}/data" '''
@app.route(f'{ROOT_API}/blob/<blob_id>/data', methods = ('GET','POST','PATCH'))
def data_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('Unauthorized', status = 401)
    
    roles_user, name_user = get_data_token(auth_token)
    
    if request.method == 'GET':
        file_path, code_rtr = business.get_file_blob(blob_id, auth_token, roles_user)
        
        with open(file_path, 'rb') as file:
            file_content = file.read()

        response = Response(file_content, status=200, mimetype='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename={file_path}'
        return response
        
    if request.method == 'POST' or request.method == 'PATCH':
        #Sacamos los roles del user que quiere modificar el Blob
        roles_user, name_user = get_data_token(auth_token)
                
        # Comprobación del archivo en la petición
        if 'file' not in request.files:
            return Response('Bad Request: No file part', status=400)
        
        #Sacamos el file de la peticion
        file = request.files['file']
        #Sacamos el nombre del archivo
        filename = os.path.basename(file.filename) 
        #Juntamos la ruta de nuestro directorio de persistencia con el nombre del archivo
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        
        rtr_code = business.modify_file_blob(blob_id, auth_token, roles_user, file)
        
        if rtr_code == 200:
            return Response('Modified', status = 200)
        
@app.route(f'{ROOT_API}/blob/<blob_id>/roles', methods = ('GET', 'PATCH', 'POST'))
def roles_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    if not auth_token:
        return Response('', status = 401)
    
    roles_user, name_user = get_data_token(auth_token)
    
    if request.method == 'GET':
        roles, rtr_code = business.get_roles_blob(blob_id, auth_token, roles_user)
        
        if rtr_code == 200:
            response = Response(json.dumps(roles), status=200, mimetype='application/json')
            return response

    if request.method == 'PATCH' or request.method == 'POST':
        #Sacamos los roles del user que quiere modificar el Blob
        roles_user, name_user = get_data_token(auth_token)
        new_roles = request.json.get('writable_by')
        
        rtr_code = business.modify_roles_blob(blob_id, auth_token, roles_user, new_roles)
        
        if rtr_code == 200:
            return Response(f'Modified: {new_roles}', status = 200)
            

@app.route(f'{ROOT_API}/blob/<blob_id>/name', methods = ('GET', 'PATCH', 'POST'))
def name_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        #AQUI HAY QUE LLAMAR A LA CAPA DE NEGOCIO PARA VERIFICAR SI ESE AUTH_TOKEN ESTA PERMITIDO
        return Response('', status = 401)
    
    if request.method == 'GET':
        roles_user, name_user = get_data_token(auth_token)
        
        name_blob, rtr_code = business.get_name_blob(blob_id, auth_token, roles_user)
        
        if rtr_code == 200:
            return Response(f'{name_blob}', status = 200)
        else:
            return Response('', status = 401)


    if request.method == 'PATCH' or request.method == 'POST':
        #Sacamos los roles del user que quiere modificar el Blob
        roles_user, name_user = get_data_token(auth_token)
        new_name = request.json.get('name')
        
        rtr_code = business.modify_name_blob(blob_id, auth_token, roles_user, new_name)
        
        if rtr_code == 200:
            return Response(f'Modified: {new_name}', status = 200)

        return Response('', status = 200)

def get_data_token(authToken) -> Union[List[str], str]:
    response = requests.get(
        f'{URL_TOKEN_SERVICE}/api/v1/token/{authToken}'
    )
    
    if response.status_code != 200:
        raise Exception(f'Token {authToken} not found')
    
    roles = response.json().get('roles')
    owner = response.json().get('username')
        
    return roles, owner

if __name__ == '__main__':
    app.run(host = f'{args.listening}', port = args.port, debug = True)