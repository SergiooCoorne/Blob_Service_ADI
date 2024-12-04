# Imagen de ubuntu 22.04
FROM ubuntu:22.04

# Crea un usuario no root para ejecutar el servicio
RUN groupadd -r blobUser && useradd -r -g blobUser blobUser

#Definimos la variable donde se va a guardar la persistencia
ENV BLOB_SERVICE_STORAGE=/service/storage

#Variable de entorno para acceder al servicio de tokens
ENV TOKEN_SERVICE=http://192.168.18.114:3002

#Creamos la carpeta storage
RUN mkdir -p $BLOB_SERVICE_STORAGE

#Le damos permisos a la carpeta service y storage
RUN chown -R blobUser:blobUser /service

# Copiamos todo lo relacionado con el servicio
COPY . .

# Actualizamos el sistema e instalamos lo necesario
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Instalacion del servicio y sus dependencias
RUN pip install .

#Exponemos el puerto 3003
EXPOSE 3003

#Cambiamos al usuario blobUser
USER blobUser

#Lanzamos el servicio
CMD blob_service --storage $BLOB_SERVICE_STORAGE
