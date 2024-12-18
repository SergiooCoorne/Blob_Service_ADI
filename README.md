# Blob Service

## Instalación

Para instalar el servicio, solo hay que crear un entorno virtual de python:

```
python3 -m venv .venv
```
Y posteriormente activarlo
```
source .venv/bib/activate
```

Después, se ejecuta el siguiente comando para instalar el servicio
```
pip install .
```

O, si vamos a modificarlo durante el desarrollo,

```
pip install -e .
```

## Ejecución

Para ejecutar el servicio solo hay que ejecutar el comando: 
```
blob_service 
```

O si por le contrario queremos especificar el puerto de escucha, dirección y ruta de almacenamiento, ejecutaremos: 
```
blob_service -p <puerto> -l <direccion> -s <ruta>
```

## Instalacion de los test

Si se van a correr test de forma manual, hay que instalar la siguiente dependencia:

- Para ello: `pip install .[tests]`

# Ejecucion de los test

Para ejecutarlos, desde el direcotrio raiz del proyecto solo hay que ejecutar `pytest` 

Si queremos ver la cobertura del proyecto ejecutamos `pytest --cov=blobservice --cov-report=html`. Esto nos creará una carpeta donde tendremos un __index.html__ en el cual se podrá ver
la cobertura del código

# Script `run_test`
Este script no lanza ningun test, unicamente buildea el contenedor de docker, lo lanza, y posteriormente lanza el mock del token_service para que el funcionamiento sea correcto. 

Hay que destacar que el mock DEBE DE ESTAR INSTALADO de forma previa, ya que si no, la orden del script que lanza el mock, no funcionará.

## Aclaración importante
Para que el servicio funcione de forma correcta, es necesario que esté activo el servicio de tokens, ya sea bien por el mock proporcionado para la practica, o por un servicio de tokens desarollado al completo
