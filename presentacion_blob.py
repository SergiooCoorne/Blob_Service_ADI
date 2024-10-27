#!/usr/bine/env python
import argparse
from flask import Flask, Response, request

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type = int, required = True, help = "Numero de puerto")
parser.add_argument('-l', '--listening', type = str, required = True, help = "Direccion donde se producirá la escucha")

args = parser.parse_args()

ROOT_API = '/api/v1'

'''Recurso de la API correspondiente con "API_ROOT/blob" '''
@app.route(f'{ROOT_API}/blob', methods = ('PUT',))
def add_blob():
    auth_token = request.headers.get('AuthToken')
    
    #Comprobacion de la presencia del token de autenticacion
    if not auth_token:
        return Response('Unauthorized', status = 401)
    
    #Comprobacion de la presencia de un JSON
    if not request.json:
        return Response('Bad Request', status = 400)
    
    # #Obtencion de los datos del JSON
    # name = request.json.get('name')
    # writer = request.json.get('writable_by')
    # data = request.json.get('multipart')
    
    # #Impresion de los datos para comprobar que estan llegando bien
    # print(f'Name: {name}, Data: {data}')
    # for i in writer:
    #     print(f'Writer: {i}')
    
    #AQUI IRIA LA LLAMADA A LA CAPA DE NEGOCIO PARA AVERIGUAR SI LA OPERACION SE PUEDE REALIZAR O NO
    return Response(f'Created. Data: ', status=201)

'''Recurso de la API correspondiente con "API_ROOT/blob/{blob_id}" '''
@app.route(f'{ROOT_API}/blob/<blob_id>', methods = ('DELETE',))
def delete_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('Unauthorized', status = 401)
    
    
    #A PARTIR DE AQUI HABRA QUE LLAMAR A LA COPA DE NEGOCIO PARA QUE VERIFIQUE SI EL AUTH_TOKEN ES VALIDO Y SI EL BLOB_ID EXISTE
    return Response(f'Deleted {blob_id}', status = 204)
    
'''Recurso de la API correspondiente con "API_ROOT/blob/{blob_id}/data" '''
@app.route(f'{ROOT_API}/blob/<blob_id>/data', methods = ('GET','POST','PATCH'))
def data_blob(blob_id):
    auth_token = request.headers.get('AuthToken')
    
    if not auth_token:
        return Response('Unauthorized', status = 401)
    
    if request.method == 'GET':
        #A PARTIR DE AQUI HABRA QUE LLAMAR A LA CAPA DE NEGOCIO PARA QUE DEVUELVA LOS DATOS DEL BLOB_ID O NO
        return Response('', status = 200)
    
    if request.method == 'POST' or request.method == 'PATCH':
        multipart = request.json.get('multipart')
        #A PARTIR DE AQUI HABRA QUE LLAMAR A LA CAPA DE NEGOCIO PARA QUE SUSTITUYA LOS DATOS DEL BLOB_ID O NO
        return Response('', status = 200)
    

if __name__ == '__main__':
    app.run(host = f'{args.listening}', port =args.port)