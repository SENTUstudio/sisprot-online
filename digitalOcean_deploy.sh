#!/bin/bash

if [ -z "$DIGITAL_OCEAN_IP_ADDRESS" ]
then
  echo "DIGITAL_OCEAN_IP_ADDRESS not defined"
  exit 0
fi

git archive --format tar --output ./project.tar main

echo "Cargando el proyecto... "
rsync ./project.tar root@$DIGITAL_OCEAN_IP_ADDRESS:/tmp/project.tar
echo "Carga completada..."

echo "Construyendo imagen..."
ssh -o StrictHostKeyChecking=no root@$DIGITAL_OCEAN_IP_ADDRESS << 'ENDSSH'
  mkdir -p /app
  rm -rf /app/* && tar -xf /tmp/project.tar -C /app
  docker-compose -f /app/production.yml build
  docker-compose -f /app/production.yml up -d --remove-orphans

ENDSSH
echo "Imagen Construida Satisfactoriamente..."


