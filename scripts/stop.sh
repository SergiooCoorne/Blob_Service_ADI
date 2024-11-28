#!/bin/bash

# Verifica si el contenedor está corriendo
if ! sudo docker ps --filter "name=service" | grep service; then
  echo "Error: el contenedor no está en ejecución."
  exit 1
fi

# Detén el contenedor
sudo docker stop service

# Eliminamos nuestro volumen montado para la persistencia
STORAGE="$(pwd)/storage"
sudo rm -rf "$STORAGE"