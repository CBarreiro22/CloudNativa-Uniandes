# Componente "RF-005" - Consulta de publicación

## Descripción
Este componente nos permitirá como usuario consultar una de mis publicaciones, estás contenga manera ordenada descendente por utilidad, las ofertas que han realizado otros usuarios, para no invertir tiempo innecesario eligiendo la mejor.

## Criterios de aceptación
1. El usuario brinda el identificador de la publicación que desea consultar y retorna la información de la publicación, sus ofertas, y el trayecto asociado. 
2. Las ofertas se encuentran ordenadas de forma descendente por la utilidad que brindan. 
3. El valor de la utilidad se encuentra en la respuesta junto con el detalle de cada oferta. 
4. Si el usuario no es el dueño de la publicación se debe presentar un error. Solo el propietario debe ver la información de sus propias publicaciones.

## Endpoint
Para el consumo de este servicio va a escuchar por el puerto 3004

### Consultar aplicación
<table>
<tr>
<th>Método</th>
<td>GET</td>
</tr>
<tr>
<th>Ruta</th>
<td>/rf005/posts/{id}</td>
</tr>
<tr>
<th>Parámetros</th>
<td>id: identificador de la publicación a consultar</td>
</tr>
<tr>
<th>Encabezados</th>
<td><code>Authorization: Bearer token</code></td>
</tr>
<tr>
<th>Puerto</th>
<td>3005</td>
</tr>
<tr>
<th>Cuerpo</th>
<td>N/A</td>
</tr>
</table>

#### Respuesta
<table>
<tr text-align="center">
<th>Código</th>
<th>Descripción</th>
<th>Cuerpo</th>
</tr>
<tr text-align="center">
<td>401</td>
<td>El token no es válido o está vencido.</td>
<td>N/A</td>
</tr>
<tr>
<td>404</td>
<td>La publicación no existe.</td>
<td>N/A</td>
</tr>
<tr>
<td>403</td>
<td>El usuario no tiene permiso para ver el contenido de esta publicación.</td>
<td>N/A</td>
</tr>
<tr>
<td>200</td>
<td>Objeto con todos los datos de una publicación.</td>
<td>

```json
{
    "data": {
        "id": "identificador de la publicación",
        "expireAt": "fecha y hora máxima en que se reciben ofertas en formato IDO",
        "route": {
            "id": "identificador del trayecto",
            "flightId": "identificador del vuelo",
            "origin": {
                "airportCode": "código del aeropuerto de origen",
                "country": "nombre del país de origen"
            },
            "destiny": {
                "airportCode": "código del aeropuerto de destino",
                "country": "nombre del país de destino"
            },
            "bagCost": "costo de envío de maleta"
        },
        "plannedStartDate": "fecha y hora en que se planea el inicio del viaje en formato ISO",
        "plannedEndDate": "fecha y hora en que se planea la finalización del viaje en formato ISO",
        "createdAt": "fecha y hora de creación de la publicación en formato ISO",
        "offers": [
            {
                "id": "identificador de la oferta",
                "userId": "identificador del usuario que hizo la oferta",
                "description": "descripción del paquete a llevar",
                "size": "LARGE ó MEDIUM ó SMALL",
                "fragile": "booleano que indica si es un paquete delicado o no",
                "offer": "valor en dólares de la oferta para llevar el paquete",
                "score": "utilidad que deja llevar este paquete en la maleta",
                "createdAt": "fecha y hora de creación de la publicación en formato ISO"
            }
        ]
    }
}
```

</td>
</tr>
</table>