# Levantar la Infraestructura de la Arquitectura
# Comandos de Flutter
.DEFAULT_GOAL := help

logo:
	@echo "┌──────────────────────────────────────────────┐"
	@echo "│ ███████╗███████╗███╗   ██╗████████╗██╗   ██╗ │"
	@echo "│ ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║   ██║ │"
	@echo "│ ███████╗█████╗  ██╔██╗ ██║   ██║   ██║   ██║ │"
	@echo "│ ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║ │"
	@echo "│ ███████║███████╗██║ ╚████║   ██║   ╚██████╔╝ │"
	@echo "│ ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝  │"
	@echo "└─────────────────────────────────────┤studio├─┘"
	@echo " SISPROT GLOBAL FIBER                           "
	@echo ""

## Muestra mensajes de ayuda
help: logo
	@awk '/^##.*$$/,/^[~\/\.0-9a-zA-Z_-]+:/' $(MAKEFILE_LIST) | awk '!(NR%2){print $$0p}{p=$$0}' | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

## Detiene, Construye y reinicia servicio de docker-compose
ds: logo
	docker-compose down && docker-compose build --no-cache && docker-compose up -d

## Muestra estado de contenedores orquestado con docker-compose
dc-ps: logo
<<<<<<< HEAD
	docker-compose ps

## Detiene todos los contenedores orquestado con docker-compose
dc-down: logo
	docker-compose down

## Construir contenedores y corregir problemas de permisos de acceso a carpetas de la infraestructura
inicio: logo
	docker-compose build --no-cache
	sudo chmod u=rwx,g=rwx,o=rwx airflow/logs
	sudo chown -R 5050:5050 pgadmin
=======
	docker-compose ps
>>>>>>> a1db1fed55ce2cc12cc29bd64f6dd91dbd9acf2c
