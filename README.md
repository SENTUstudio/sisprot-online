# Sisprot Online Backend

Se contempla el despliegue de la arquitectura de software necesaria para el funcionamiento local del proyecto

## Requisitos

- Python 3.10 o superior
- pip
- virtualenv

## Instalación

- Clona este repositorio: `git clone https://github.com/rungrothan/sisprot-online`
- Crea un entorno virtual: `cd sisprot-online && python -m venv .venv`
- Activa el entorno virtual: `source .venv/bin/activate`
- Instala las dependencias: `pip install -r requirements.txt`

## Configuración

Crea un archivo .env en la raíz del proyecto y define las variables de entorno necesarias. Puedes encontrar un ejemplo en el archivo .env.example.

## Ejecución

- Activa el entorno virtual: `source venv/bin/activate`
- Lanza el servidor: `uvicorn app:app --port 5000 --reload`

## Uso

Abre un navegador web y visita http://localhost:5000/docs.
Selecciona la operación que quieras probar, ingresa los parámetros necesarios y haz clic en "Try it out!".
Verás la respuesta de la API en la sección "Responses".

## Contribución

Si quieres contribuir a este proyecto, por favor sigue estos pasos:

1. Crea una rama para tu cambio: `git checkout -b mi-cambio`
2. Realiza tus cambios y haz commit: `git commit -am 'Agregué una nueva funcionalidad'`
3. Haz push a la rama: `git push origin mi-cambio`
4. Crea un pull request en GitHub.

# Arquitectura del proyecto: Airflow - Minio - Fastapi - Postgres

## Descripción

Se plantea una arquitectura de despliegue DevOps, donde se plantea un pipeline orientado a la data. Contiene una filosofía de orquestación a través de Airflow con el contenedor Docker y orientado enteramente a Python (FastApi).

TODO: La idea principal es crear la documentación del bosquejo que describe la actual situación del proyecto para luego aplicar principios de arquitectura y diseño donde un set de API REST básicos contengan lo necesario para generar las consultas CRUD con la información incluida en la data.

El proyecto es diseñado para ser escalable y extensible, con el pontencial de agregar más fuentes de datos e implementar otras herramientas como elasticsearch para el control de logs y kafka para para streaming.

#

Este proyecto contiene los siguientes container:
This project contains the following containers:

- Postgres: Postgres database para Airflow metadata y del proyecto

  - Image: postgres:13
  - Database Port: 5432

- Airflow: Airflow webserver y Scheduler.

  - Image: apache/airflow:2.2.3
  - Port: 8080

- MiniO: Local Datalake (se prevee guardar data semi estructurada y no estructurada)

  - Image: postgres:13
  - Web console Port: 9000

- Neo4j: Postgres database para Airflow metadata

  - Image: neo4j:4.4.0
  - Database Port: 7474

- FastAPI: Requests via API
  - Image: 0.95.0
  - Database Port: 8000

## Estructura de archivos

```bash
sisprot-online
├── airflow
│   ├── dags
│   │   ├── parse_uniprot_xml.py
│   │   ├── Q9Y261.xml
│   │   └── uniprot_data_pipeline.py
│   ├── logs
│   │   ├── dag_processor_manager
│   │   └── scheduler
│   ├── plugins
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
├── config
│   └── pgadmin.env
├── data
│   ├── architecture.png
│   ├── architecture_small.png
│   └── Q9Y261.xml
├── fastapi
│   ├── __pycache__
│   │   ├── app.cpython-310.pyc
│   │   ├── app.cpython-39.pyc
│   │   └── gunicorn_conf.cpython-39.pyc
│   ├── sisprot
│   │   ├── models
│   │   ├── __pycache__
│   │   ├── routes
│   │   ├── schemas
│   │   ├── tasks
│   │   ├── auth.py
│   │   ├── db.py
│   │   ├── __init__.py
│   │   ├── messages.py
│   │   ├── pagination.py
│   │   ├── roles.py
│   │   └── utils.py
│   ├── app.py
│   ├── Dockerfile
│   ├── _.env
│   └── requirements.txt
├── logs
├── minio
│   ├── Dockerfile
│   ├── requirements.txt
│   └── setup.sh
├── pgadmin
│   ├── docker_pgadmin_servers.json
│   └── pgadmin
│       ├── azurecredentialcache
│       ├── sessions
│       ├── storage
│       └── pgadmin4.db
├── postgresql
│   └── data
├── venv
│   ├── bin
├── docker-compose.yml
├── Makefile
├── README.md
```

## Arquitectura de componentes

![Screenshot](architecture_small.png)

## Setup

### Requerimientos

    $ Debes tener instalado docker en tu máquina. Ignore si usa CDE (Cloud Development Environment), Gitpod, GitHub Codespaces, entre otros.

### Clone proyecto

    `git clone https://github.com/rungrothan/sisprot-online`

### Build containers

Desde la carpeta `sisprot-online`

    `$ docker-compose build --no-cache`

### Iniciar containers

Un inicio con vista a logs:

    `$ docker-compose up`

Un inicio modo background:

    `$ docker-compose up -d`

### Credenciales de acceso:

| Applicación | URL                                                          | Credenciales                          |     |
| ----------- | ------------------------------------------------------------ | ------------------------------------- | --- |
| Airflow     | [http://localhost:8080](http://localhost:8080)               | ` User: admin` <br> ` Pass: admin`    |     |
| Neo4j       | **Database:** [http://localhost:7474](http://localhost:7474) | ` User: neo4j` <br> ` Pass: password` |     |
| MinIO       | [http://localhost:9000](http://localhost:9000)               | ` User: admin` <br> ` Pass: password` |     |
| FastAPI     | [http://localhost:8000/docs](http://localhost:8000/redoc)    |                                       |     |

### Problemas conocidos:

#### airflow:

Problemas de permiso de escritura en la carpeta logs.
Se soluciona con:
`sudo chmod u=rwx,g=rwx,o=rwx logs`

#### pgadmin4:

Problema de permisos de escritura en la carpeta "pgadmin"
Se soluciona con:
`sudo chown -R 5050:5050 pgadmin`

## Referencias

[neo4j.com] (https://neo4j.com/docs/ogm-manual/current/reference/)

[uniprot.org] (https://www.uniprot.org/help/technical)

[airflow.apache.org] (https://airflow.apache.org/docs/apache-airflow/stable/)

[min.io] ([https://min.io/docs/minio/linux/developers/go/API.html](https://min.io/docs/minio/linux/reference/minio-server/minio-server.html)
