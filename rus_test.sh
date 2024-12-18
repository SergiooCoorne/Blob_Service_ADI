#!/bin/bash

#Creacion de la maquina y lanzamiento del servicio
sudo ./scripts/build.sh
sudo ./scripts/run.sh &

#Lanzamos ahora el mock necesario para realizar las pruebas (En este caso el token_service)
token_service &
