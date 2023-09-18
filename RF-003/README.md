# Componente "RF-003" - Crear publicaciones

## Descripción
Este componente nos permitirá como usuario crear publicaciones para que otros usuarios puedan ofertar por ellas

## Criterios de aceptación
1. El usuario brinda los datos de la publicación y el trayecto que hará.
2. Se valida si el trayecto ya existe o no, sino existe se crea con los valores indicados y se usa ese para la creación de la publicación, si ya existe se descartan los datos brindados y se usa el que está almacenado.
3. La publicación queda asociada al usuario de la sesión.
4. La plataforma solo permite crear publicaciones cuando la fecha de inicio de viaje es en el futuro.
5. La plataforma solo permite crear publicaciones cuando la fecha de expiración de la publicación es posterior a la fecha actual y anterior o igual a la fecha de inicio de viaje.
6. Si el usuario ya tiene otra publicación para el mismo trayecto se rechaza la creación.
7. Solo un usuario autenticado puede realizar esta operación.
8. En cualquier caso de error la información al finalizar debe ser consistente.

## Endpoint
Para el consumo de este servicio va a escuchar por el puerto 3006

### Creación de una publicación
<table>
<tr>
<th>Método</th>
<td>POST</td>
</tr>
<tr>
<th>Ruta</th>
<td>/rf003/posts</td>
</tr>
<tr>
<th>Parámetros</th>
<td>N/A</td>
</tr>
<tr>
<th>Encabezados</th>
<td><code>Authorization: Bearer token</code></td>
</tr>
<tr>
<th>Puerto</th>
<td>3006</td>
</tr>
<tr>
<th>Cuerpo</th>
<td>

```json
{
    "flightId": "identificador del vuelo",
    "expireAt": "fecha y hora máxima en la que se recibirán ofertas sobre la publicación en formato ISO",
    "plannedStartDate": "fecha y hora planeada de salida del origen en formato ISO",
    "plannedEndDate": "fecha y hora planeada de llegada en formato ISO",
    "origin": {
       "airportCode": "código del aeropuerto de origen",
       "country": "nombre del país de origen"
    },
    "destiny": {
       "airportCode": "código del aeropuerto de origen",
       "country": "nombre del país de origen"
    },
    "bagCost": "costo de envío de maleta en dólares"
}
```

</td>
</tr>
</table>

#### Respuesta
<table>
<tr text-align="center">
<th>Código</th>
<th>Descripción</th>
<th>Cuerpo</th>
</tr>
<tr>
<td>400</td>
<td>En el caso que alguno de los campos no esté presente en la solicitud, o no tenga el formato esperado.</td>
<td>N/A</td>
</tr>
<tr text-align="center">
<td>401</td>
<td>El token no es válido o está vencido.</td>
<td>N/A</td>
</tr>
<tr>
<td>403</td>
<td>El usuario no tiene permiso para ver el contenido de esta publicación.</td>
<td>N/A</td>
</tr>
<tr>
<td>412</td>
<td>En el caso que la fecha de inicio y fin del trayecto no sean válidas; fechas en el pasado o no consecutivas.</td>
<td>

```json
{
    "msg": "Las fechas del trayecto no son válidas"
}
```

</td>
</tr>
<tr>
<td>412</td>
<td>En el caso que la fecha de expiración no sea en el futuro o no sea válida.</td>
<td>

```json
{
    "msg": "La fecha expiración no es válida"
}
```

</td>
</tr>
<tr>
<td>412</td>
<td>Si el usuario ya tiene otra publicación para el mismo trayecto.</td>
<td>

```json
{
    "msg": "El usuario ya tiene una publicación para la misma fecha"
}
```

</td>
</tr>
<tr>
<td>200</td>
<td>Si la creación de la publicación es exitosa.</td>
<td>

```json
{
    "data": {
       "id": "id de la publicación",
       "userId": "id del usuario que crea la publicación",
       "createdAt": "fecha y hora de creación de la publicación en formato ISO",
       "expireAt": "último día en que se reciben ofertas sobre la publicación",
       "route": {
          "id": "id del trayecto",
          "createdAt": "fecha y hora de creación del trayecto en formato ISO"
       }
    },
    "msg": "Resumen de la operación *."
}
```

</td>
</tr>
</table>