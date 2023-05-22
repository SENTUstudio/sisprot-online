VISITA_AGENDADA_MSG = """Te visitaremos pronto.

👋 Hola, estimado (a) {nombre_cliente}

📢 Queremos informarte que hemos agendado una visita técnica a tu hogar/empresa, ya que has reportado una falla con el número de seguimiento {id_falla}.

🗓 Día: {dia_visita}

Está atento (a) a tu celular, puesto que nuestro equipo técnico se estará comunicando 1 hora antes de ir a su hogar/empresa para confirmar que se encuentre en el lugar, en caso de no recibir una respuesta se reprogramará la visita para el día siguiente.

Le deseamos un feliz día,
Gracias por preferirnos.
"""

VISITA_AGENDADA_GRUPO_MSG = """🚗 *VISITA TÉCNICA AGENDADA* 🏍

📅 *Día de la visita:* {dia_visita}
⏰ *Rango de Hora:* {hora_inicio} - {hora_fin}
- - - - - - - - - - - - - - - -
*N° Reporte de Falla:* {id_falla}
*Nombre cliente*: {nombre_cliente}
- - - - - - - - - - - - - - - -
*IP Cliente*: {ip_cliente}
*VLAN*: {vlan_cliente}
- - - - - - - - - - - - - - - -
*Google Maps*
{url_google_map}
- - - - - - - - - - - - - - - -
*Visita Agendada por*
👤 {nombre_agente}
"""

VISITA_REPROGRAMADA_MSG = """🏍 Te visitaremos pronto.

👋 Hola, estimado (a) {nombre_cliente}

📢 Queremos informarte que hemos reprogramado la visita técnica a tu hogar/empresa, ya que has reportado una falla con el número de seguimiento {id_falla}.

🗓 Día: {dia_visita}

Está atento (a) a tu celular, puesto que nuestro equipo técnico se estará comunicando 1 hora antes de ir a su hogar/empresa para confirmar que se encuentre en el lugar, en caso de no recibir una respuesta se reprogramará la visita para el día siguiente.

Le deseamos un feliz día,
Gracias por preferirnos.
"""

VISITA_REPROGRAMADA_GRUPO_MSG = """🚗 *VISITA TÉCNICA REPROGRAMADA* 🏍

📅 *Día de la visita:* {dia_visita}
⏰ *Rango de Hora:* {hora_inicio} - {hora_fin}
- - - - - - - - - - - - - - - -
*N° Reporte de Falla:* {id_falla}
*Nombre cliente:* {nombre_cliente}
*Barrio/Localidad:* {barrio_localidad}
- - - - - - - - - - - - - - - -
*IP Cliente*: {ip_cliente}
*VLAN*: {vlan_cliente}
- - - - - - - - - - - - - - - -
*Google Maps*
{url_google_map}
- - - - - - - - - - - - - - - -
*Visita reprogramada por*
👤 {nombre_agente}
"""

REPORTE_CERRADO_MSG = """📁 Hemos cerrado tu reporte de falla

👋 Hola, estimado (a) {nombre_cliente}

📢 Queremos informarte que hemos cerramos el reporte de falla con el número de seguimiento {id_falla}

*Motivo:* {motivo_cierre}
Comentario: {comentario}

Le deseamos un feliz día,
Gracias por preferirnos.

"""

REPORTE_CERRADO_GROUP_MSG = """📁 *REPORTE DE FALLA CERRADO*

*N° Reporte de Falla:* {id_falla}
*Nombre Cliente:* {nombre_cliente}
*Barrio/Localidad:* {barrio_localidad}
- - - - - - - - - - - - - - - -
*Motivo de Cierre:*
{motivo_cierre}

*Comentario:*
{comentario}
- - - - - - - - - - - - - - - -
*Reporte Cerrado por:*
👤 {nombre_agente}"""