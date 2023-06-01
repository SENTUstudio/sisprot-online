import logging, smtplib, ssl
import base64
import time
from fastapi import APIRouter, Depends, HTTPException, status
import requests
from sisprot.db import get_db
from sisprot.auth import jwt_required, get_current_user
from sisprot.models import ProspectosResidenciales, PlantillaMensaje
from sisprot.schemas import ProspectosResidencialesInSchema
from sisprot.utils import config, Default
from sisprot.files import static_path, save_static_file


router = APIRouter(prefix="/api")

msg_template = """Formulario de Factibilidad
- - - - - - - - - - - - - - - - - - - - - 
👤 Nombres Completos:
{nombre_completo}

👤 Apellidos Completos:
{apellido_completo}

🆔 Cédula de Identidad/RIF:
{cedula}

📍 Dirección Completa:
{direccion_completa}

🏙 Barrio/Localidad:
{barrio_localidad}

🌉 Municipio:
{municipio}

📧 Correo Eléctronico:
{email}

📞 Número de Teléfono:
{telefono}

🌐 Plan Tentativo:
{plan_tentativo}
- - - - - - - - - - - - - - - - - - - -
🗺 Coordenadas ( Lat/Lng ):
{latitud}, {longitud}
- - - - - - - - - - - - - - - - - - - -
Estados de una factibilidad
✅ Factible
☎ Se llamo, pero hay que volver a llamar
❌ No factible
📒 Cliente Contratado
🅿 En proyectos
📌 En Pipedrive


"""

msg_to_user = """
👋 Hola, estimado {nombre_cliente} de la comunidad {barrio_localidad}

📣 Queremos informarte que hemos recibido tu solicitud de factibilidad de Servicio de Internet de manera correcta en nuestra base de datos ✅, un 👤 asesor de ventas se estará comunicando contigo lo más pronto posible.

+584243076327
Atención al Cliente

Síguenos en nuestras redes sociales de Instagram

https://instagram.com/sisprotgf

o  🌐 visítanos en nuestras página web:

www.sisprotgf.com

Gracias por preferirnos,
Sisprot Global Fiber c.a
"""


@router.get(
    "/prospectos-residenciales",
    dependencies=[Depends(jwt_required)],
    tags=["Prospectos Residenciales"],
)
def index(page: int = 1, session=Depends(get_db)):
    """
    Devuelve una lista paginada de Clientes importados
    """
    with session:
        stmt = session.query(ProspectosResidenciales)

        results = stmt.paginate(page=page).as_dict()
    return results


@router.put(
    "/prospectos-residenciales/{id}",
    dependencies=[Depends(jwt_required)],
    tags=["Prospectos Residenciales"],
)
def edit(id: int, data: ProspectosResidencialesInSchema, session=Depends(get_db)):
    data = data.dict(exclude_none=True)
    item = session.query(ProspectosResidenciales).filter_by(id=id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Prospecto no se encuentra")
    for k, v in data.items():
        setattr(item, k, v)
    session.commit()


@router.delete(
    "/prospectos-residenciales/{id}",
    dependencies=[Depends(jwt_required)],
    tags=["Prospectos Residenciales"],
)
def delete(id: int, session=Depends(get_db)):
    item = session.query(ProspectosResidenciales).filter_by(id=id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Prospecto no se encuentra")

    session.delete(item)
    session.commit()


@router.post("/prospectos-residenciales", tags=["Prospectos Residenciales"])
def create(data: ProspectosResidencialesInSchema, session=Depends(get_db)):
    """
    Crea un prospecto, posteriormente envia un mensaje por Whatsapp con
    los datos del prospecto, tambien envia los datos via api de OZMAP
    """

    item = ProspectosResidenciales(**data.dict(exclude={"foto_cedula", "foto_rif"}))

    try:
        filename = data.foto_cedula[0]
        image_as_bytes = str.encode(data.foto_cedula[1])  # convert string to bytes
        img_recovered = base64.b64decode(image_as_bytes)  # decode base64string
        file_ext = filename.split(".")[-1]
        random_filename = f"cedula_{data.cedula}_{time.time()}.{file_ext}"
        item.foto_cedula = random_filename
        save_static_file(f"prospectos/{random_filename}", img_recovered)

        filename = data.foto_rif[0]
        image_as_bytes = str.encode(data.foto_rif[1])  # convert string to bytes
        img_recovered = base64.b64decode(image_as_bytes)  # decode base64string
        file_ext = filename.split(".")[-1]
        random_filename = f"rif_{data.cedula}_{time.time()}.{file_ext}"
        item.foto_rif = random_filename
        save_static_file(f"prospectos/{random_filename}", img_recovered)

    except Exception:
        logging.exception("error uploading image")
        return {"message": "There was an error uploading the file"}

    if data.barrio_localidad == "otro":
        item.otro_barrio_localidad = data.otro_barrio_localidad
    else:
        item.otro_barrio_localidad = None
    session.add(item)
    session.commit()

    factibilidad_plantilla = (
        session.query(PlantillaMensaje)
        .filter(PlantillaMensaje.nombre == "FORM_FACTIBILIDAD")
        .first()
    )

    factibilidad_plantilla_user = (
        session.query(PlantillaMensaje)
        .filter(PlantillaMensaje.nombre == "FORM_FACTIBILIDAD_USER")
        .first()
    )

    msg = ""
    for k, v in data.dict().items():
        msg += f"{k}: {v}\n"

    try:
        API_TOKEN = config(session, key="wiivo_api_token")
        headers = {"Content-Type": "application/json", "Token": API_TOKEN}

        barrio_localidad = (
            data.otro_barrio_localidad
            if data.barrio_localidad == "otro"
            else data.barrio_localidad
        )

        payload = {
            "group": "120363049087045640@g.us",
            "message": factibilidad_plantilla.mensaje.format_map(
                Default(
                    **data.dict(exclude={"coordenadas", "barrio_localidad"}),
                    barrio_localidad=barrio_localidad,
                )
            ),
        }

        requests.post(
            "https://api.wiivo.net/v1/messages", json=payload, headers=headers
        )

        payload = {
            "phone": f"+{data.telefono}",
            "message": factibilidad_plantilla_user.mensaje.format_map(
                Default(
                    nombre_cliente=data.nombre_completo,
                    barrio_localidad=barrio_localidad,
                )
            ),
        }

        requests.post(
            "https://api.wiivo.net/v1/messages", json=payload, headers=headers
        )
    except:
        logging.exception("error al comunicarse con wiivo")

    try:
        payload = {
            "tags": ["640f489e321bec001403b9c2"],
            "name": f"{data.nombre_completo} {data.apellido_completo}",
            "coords": [float(data.longitud), float(data.latitud)],
            "code": "none",
            "address": f"{data.direccion_completa}",
            "observation": f"{data.telefono}",
        }
        OZMAP_TOKEN = config(session, key="ozmap_token")
        headers = {"Authorization": OZMAP_TOKEN}
        r = requests.post(
            "http://sisprtoglobalfiber.ozmap.com.br:9090/api/v2/prospects",
            json=payload,
            headers=headers,
        )
    except:
        logging.exception("error al comunicarse con la api de ozmap")

    try:
        context = ssl.create_default_context()
        port = config(session, key="smtp_port_tls")  # For starttls
        smtp_server = config(session, key="smtp_server")
        smtp_password = config(session, key="smtp_password")
        sender_email = config(session, key="smtp_sender_email")
        to_send = "prospectos@sisprotgf.com"
        with smtplib.SMTP(smtp_server, port) as server:
            msg = "Subject: Notificación\n\n" + msg
            print(msg)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, to_send, msg)
    except:
        logging.exception("error al enviar correo")
        pass
