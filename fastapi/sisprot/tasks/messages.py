import json
import requests
import logging
from sisprot.models import Task, Cliente, PlantillaMensaje
from sisprot.db import get_db, db_session
from sisprot.utils import config, row2dict
import smtplib, ssl

url = "https://api.wiivo.net/v1/messages"



class Default(dict):
    def __missing__(self, key):
        return key.join("{}")


def send_messages(task_id, data, filters):
    session = db_session()
    task = session.query(Task).filter_by(id=task_id).first()

    task.status = "RUNNING"
    session.commit()

    try:
        query = session.query(Cliente).outerjoin(Cliente.country)

        # Create a secure SSL context

        port = config(session, key="smtp_port_tls")  # For starttls
        
        smtp_server = config(session, key="smtp_server")
        smtp_password = config(session, key="smtp_password")
        sender_email = config(session, key="smtp_sender_email")


        if filters['router'] != (None,):
            query = query.filter(Cliente.router.in_(filters['router']))

        if filters['plan'] != (None,):
            query = query.filter(Cliente.id_plan.in_(filters['plan']))
        
        if filters['status'] != (None,):
            query = query.filter(Cliente.id_estado_cliente.in_(filters['status']))

        if filters['barrio_localidad'] != (None,):
            query = query.filter(Cliente.barrio_localidad.in_(filters['barrio_localidad']))

        if filters['estado_facturacion'] != (None,):
            query = query.filter(Cliente.estado_facturacion.in_(filters['estado_facturacion']))
        
        if filters['precio_plan'] != (None,):
            query = query.filter(Cliente.precio_plan.in_(filters['precio_plan']))

        if filters['tipo_cliente'] != (None,):
            query = query.filter(Cliente.id_tipo_cliente.in_(filters['tipo_cliente']))


        clients = query.all()



        API_TOKEN = config(session, key="wiivo_api_token")

        headers = {"Content-Type": "application/json", "Token": API_TOKEN}

        errors = []

        template = None

        if data.template_id:
            template = (
                session.query(PlantillaMensaje).filter_by(id=data.template_id).first()
            )


        for client in clients:
            phones = client.telefono.split(',')

            if data.enable_whatsapp:

                for phone in phones:

                    if not client.country:
                        errors.append({'msg': f"El cliente {client.nombre_cliente} no posee un pais asignado"})
                        continue

                    payload = {
                        "phone": f"+{client.country.codigo}{phone}",
                        # "message": "Hello world! This is a simple test message.",
                    }

                    if data.message:
                        payload["message"] = data.message.format_map(Default(row2dict(client)))
                    if data.media:
                        payload["media"] = {"file": data.media}
                    if template:
                        payload["message"] = template.mensaje.format_map(Default(row2dict(client)))
                    if data.deliver_at:
                        payload['schedule'] = {
                            'deliver_at': data.deliver_at
                        }

                    # print(payload)

                    r = requests.post(url, json=payload, headers=headers)

                    print(r.json())
                    if r.status_code != 201:
                        errors.append(r.json())

            if data.enable_email:

                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    msg = "Subject: Notificación\n" + payload["message"]
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(sender_email, smtp_password)
                    server.sendmail(sender_email, client.email_cliente, msg)

        if errors:
            task.status = "FINISH_WIH_ERRORS"
            task.errors = json.dumps(errors)
        else:
            task.status = "SUCCESS"
        session.commit()

    except Exception as ex:
        logging.exception("error sending msg")
        task.status = "ERROR"
        task.errors = str(ex)
        session.commit()

