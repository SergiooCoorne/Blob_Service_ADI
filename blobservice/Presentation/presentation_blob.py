import sys
import os
import argparse
from flask import Flask, Response, request
from typing import List, Union
import getpass
import requests
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
from blobservice.Business.business_blob import Business

name_system = getpass.getuser()
URL_TOKEN_SERVICE = 'http://127.0.0.1:3002'

app = Flask(__name__)

global UPLOAD_DIRECTORY
global business
ROOT_API = '/api/v1'

def create_app():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=3003, help="Número de puerto (por defecto 3003)")
    parser.add_argument('-l', '--listening', type=str, default='0.0.0.0', help="Dirección donde se producirá la escucha (por defecto '0.0.0.0')")
    parser.add_argument('-s', '--storage', type=str, default=f'/home/{name_system}/persistence_dir', help=f'Ruta donde se almacenará la persistencia (por defecto "/home/{name_system}/persistence_dir")')

    #Si no estamos pasando los test, le pasamos argumentos por defecto
    if os.getenv("PYTEST_CURRENT_TEST") is None:
        args = parser.parse_args()
        app.config["PORT"] = args.port
        app.config["LISTENING"] = args.listening
        app.config["STORAGE"] = args.storage
    else:
        # Valores predeterminados para pruebas
        app.config["PORT"] = 3003
        app.config["LISTENING"] = "0.0.0.0"
        app.config["STORAGE"] = f'/home/{name_system}/persistence_dir'
    
    # Almacenamos la ruta de persistencia en la variable global
    global UPLOAD_DIRECTORY
    UPLOAD_DIRECTORY = app.config["STORAGE"]

    # Creamos nuestra instancia de la capa de negocio
    global business
    business = Business(UPLOAD_DIRECTORY)

    return app

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
    
    print(f'File: {file}')

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
    try:
        rtr_code = business.delete_blob(blob_id, auth_token, roles_user)
    except Exception as e:
        print(f'Exception: {str(e)}')
        return Response('Unauthorized', status=401)

    if rtr_code == 200:
        return Response('Modified', status=200)
    elif rtr_code == 404:
        return Response('Blob not found', status=404)        
    
'''Recurso de la API correspondiente con "API_ROOT/blob/{blob_id}/data" '''
@app.route(f'{ROOT_API}/blob/<blob_id>/data', methods = ('GET','POST','PATCH'))
def data_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('Unauthorized', status = 401)
    
    roles_user, name_user = get_data_token(auth_token)
    
    if request.method == 'GET':
        try:
            file_path, code_rtr = business.get_file_blob(blob_id, auth_token, roles_user)
        except Exception as e:
            print(f'Exception: {str(e)}')
            return Response('Unauthorized', status = 401)
    
        if code_rtr == 200:
            with open(file_path, 'rb') as file:
                file_content = file.read()

            response = Response(file_content, status=200, mimetype='application/octet-stream')
            response.headers['Content-Disposition'] = f'attachment; filename={file_path}'
            return response
        elif code_rtr == 404:
            return Response('Blob not found', status=404)
        
    if request.method == 'POST' or request.method == 'PATCH':
        #Sacamos los roles del user que quiere modificar el Blob
        roles_user, name_user = get_data_token(auth_token)
                
        # Comprobación del archivo en la petición
        if 'file' not in request.files:
            return Response('No content', status=204)
        
        #Sacamos el file de la peticion
        file = request.files['file']
        
        try:
            rtr_code = business.modify_file_blob(blob_id, auth_token, roles_user, file)
        except Exception as e:
            print(f'Exception: {str(e)}')
            return Response('Unauthorized', status=401)

        if rtr_code == 200:
            return Response('Modified', status=200)
        elif rtr_code == 404:
            return Response('Blob not found', status=404)
        else:
            return Response('',status=500)
        
@app.route(f'{ROOT_API}/blob/<blob_id>/roles', methods = ('GET', 'PATCH', 'POST'))
def roles_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('', status = 401)
    
    roles_user, name_user = get_data_token(auth_token)
    
    if request.method == 'GET':
        try:
            roles, rtr_code = business.get_roles_blob(blob_id, auth_token, roles_user)
        except Exception as e:
            print(f'Exception: {str(e)}')
            return Response('Unauthorized', status=401)

        if rtr_code == 200:
            response = Response(json.dumps(roles), status=200, mimetype='application/json')
            return response
        elif rtr_code == 404:
            return Response('Blob not found', status=404)

    if request.method == 'PATCH' or request.method == 'POST':
        #Sacamos los roles del user que quiere modificar el Blob
        roles_user, name_user = get_data_token(auth_token)
        new_roles = request.json.get('writable_by')
        
        try:
            rtr_code = business.modify_roles_blob(blob_id, auth_token, roles_user, new_roles)
        except Exception as e:
            print(f'Exception: {str(e)}')
            return Response('Unauthorized', status=401)

        if rtr_code == 200:
            return Response('Modified', status=200)
        elif rtr_code == 404:
            return Response('Blob not found', status=404)
        else:
            return Response('',status=500)

@app.route(f'{ROOT_API}/blob/<blob_id>/name', methods = ('GET', 'PATCH', 'POST'))
def name_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('Bad Request', status = 401)
    
    if request.method == 'GET':
        roles_user, name_user = get_data_token(auth_token)
        
        try:
            name_blob, rtr_code = business.get_name_blob(blob_id, auth_token, roles_user)
        except Exception as e:
            print(f'Exception: {str(e)}')
            return Response(f'Unauthorized', status=401)

        if rtr_code == 200:
            return Response(f'{name_blob}', status = 200)
        elif rtr_code == 404:
            return Response('Blob not found', status = 404)
        else:
            return Response('', 500)

    if request.method == 'PATCH' or request.method == 'POST':
        #Sacamos los roles del user que quiere modificar el Blob
        roles_user, name_user = get_data_token(auth_token)
        new_name = request.json.get('name')
        
        try:
            rtr_code = business.modify_name_blob(blob_id, auth_token, roles_user, new_name)
        except Exception as e:
            print(f'Exception: {str(e)}')
            return Response('Unauthorized', status=401)

        if rtr_code == 200:
            return Response('Modified', status=200)
        elif rtr_code == 404:
            return Response('Blob not found', status=404)
        else:
            return Response('', 500)


def get_data_token(authToken) -> Union[List[str], str]:
    response = requests.get(
        f'{URL_TOKEN_SERVICE}/api/v1/token/{authToken}'
    )
    
    if response.status_code != 200:
        raise Exception(f'Token {authToken} not found')
    
    roles = response.json().get('roles')
    owner = response.json().get('username')
        
    return roles, owner

def main(app):
    app.run(host=app.config["LISTENING"], port=app.config["PORT"], debug=True)

if __name__ == '__main__':
    app = create_app()
    main(app)
