#!/bin/bash

# Verifica si el contenedor ya está corriendo
if sudo docker ps --filter "name=service" | grep service; then
  echo "Error: el contenedor ya está en ejecución."
  exit 1
fi

#Variable de entorno para definir la ruta donde se almacenara la persistencia (Que sera compartida con el contenedor)
#En nuestro cado, sera : CurrentDirectory/storage
STORAGE="$(pwd)/storage"
mkdir -p "$STORAGE"
#Damos los permisos necesarios
sudo chown -R $(whoami):$(whoami) "$STORAGE"
sudo chmod -R 777 "$STORAGE"

# Ejecuta el contenedor con las configuraciones necesarias
sudo docker run --rm \
  -v "$STORAGE:/service/storage" \
  --name service \
  --cpus=1 \
  --memory=2g \
  service