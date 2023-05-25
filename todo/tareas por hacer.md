# Campos para actualizar en los endpoint en conjunto a sus tablas asociadas

## Residenciales = {

- [X] "nombre_completo": "string",
- [X] "apellido_completo": "string",
- [X] "cedula": "string",
- [X] "email": "string",
- [X] "telefono": "string",
- [X] "direccion_completa": "string",
- [X] "barrio_localidad": "string",
- [X] "plan_tentativo": "string",
- [X] "coordenadas": "string",
- [-] "estado_vivienda": "string",
- [X] "municipio": "string",
- [-] "parroquia": "string",
- [X] "otro_barrio_localidad": "string",
- [X] "latitud": "string",
- [X] "longitud": "string",
- [-] "fecha_contratacion": "string", # TODO: NO se genera en este punto (afiliacion)
- [-] "fecha_estimada_instalacion": "string", # TODO: 15 dias habiles a partir de la contratación
- [-] "fecha_hora_registro_sistema": "string",
- [-] "id_carta_aceptacion"  # R: residencial + 5 numero + año(numerico completo) 'R-00001-2023'
  }

## Pymes = {

- [X] "nombre_completo": "string",
- [X] "apellido_completo": "string",
- [X] "cedula": "string",
- [-] "nombre_o_razon_social": "string",
- [-] "rif": "string",
- [X] "email": "string",
- [X] "telefono": "string",
- [X] "direccion_completa": "string",
- [X] "barrio_localidad": "string",
- [X] "plan_tentativo": "string",
- [X] "coordenadas": "string",
- [-] "estado_vivienda": "string",
- [X] "municipio": "string",
- [X] "parroquia": "string",
- [X] "otro_barrio_localidad": "string",
- [X] "latitud": "string",
- [X] "longitud": "string",
- [-] "fecha_contratacion": "string", # TODO: NO se genera en este punto (afiliacion)
- [-] "fecha_estimada_instalacion": "string", # TODO: 15 dias habiles a partir de la contratación
- [-] "fecha_hora_registro_sistema": "string""id_carta_aceptacion"  # P: residencial + 5 numero + año(numerico
  completo) '
  P-00001-2023'
  }

```