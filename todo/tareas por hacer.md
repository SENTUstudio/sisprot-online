# Campos para actualizar en los endpoint en conjunto a sus tablas asociadas

```bash
Residenciales = {
    "nombre_completo": "string",
    "apellido_completo": "string",
    "cedula": "string",
    "email": "string",
    "telefono": "string",
    "direccion_completa": "string",
    "barrio_localidad": "string",
    "plan_tentativo": "string",
    "coordenadas": "string",
    "estado_vivienda": "string",
    "municipio": "string",
    "parroquia": "string",
    "otro_barrio_localidad": "string",
    "latitud": "string",
    "longitud": "string",
    "fecha_contratacion": "string", # TODO: NO se genera en este punto (afiliacion)
    "fecha_estimada_instalacion": "string", # TODO: 15 dias habiles a partir de la contratación
    "fecha_hora_registro_sistema": "string",
    "id_carta_aceptacion"  # R: residencial + 5 numero + año(numerico completo) 'R-00001-2023'
}
Pymes = {
    "nombre_completo": "string",
    "apellido_completo": "string",
    "cedula": "string",
    "nombre_o_razon_social": "string",
    "rif": "string",
    "email": "string",
    "telefono": "string",
    "direccion_completa": "string",
    "barrio_localidad": "string",
    "plan_tentativo": "string",
    "coordenadas": "string",
    "estado_vivienda": "string",
    "municipio": "string",
    "parroquia": "string",
    "otro_barrio_localidad": "string",
    "latitud": "string",
    "longitud": "string",
    "fecha_contratacion": "string", # TODO: NO se genera en este punto (afiliacion)
    "fecha_estimada_instalacion": "string", # TODO: 15 dias habiles a partir de la contratación
    "fecha_hora_registro_sistema": "string""id_carta_aceptacion"  # P: residencial + 5 numero + año(numerico completo) 'P-00001-2023'
}
```