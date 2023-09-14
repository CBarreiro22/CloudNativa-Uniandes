# Componente "RF-004" - Crear Ofertas

## Descripción

Este componente nos permitirá como usuario ofertar sobre alguna publicación de otro usuario para poder contratar un servicio.

## Criterios de aceptación
1. El usuario brinda la información de la oferta que desea hacer y el identificador de la publicación a la que se realiza.
2. Se valida que la publicación existe, solo se puede crear la oferta en una publicación existente.
3. Solo es posible crear la oferta si la publicación no ha expirado.
4. La oferta queda asociada al usuario de la sesión.
5. El usuario no debe poder ofertar en sus publicaciones.
6. Se calcula la utilidad (score) de la oferta.
7. Solo un usuario autenticado puede realizar esta operación.
8. En cualquier caso de error la información al finalizar debe ser consistente.

## Endpoint
Para el consumo de este servicio va a escuchar por el puerto 3007

<table>
<tr>
<th>Método</th>
<td>POST</td>
</tr>
<tr>
<th>Ruta</th>
<td>/rf004/posts/{id}/offers</td>
</tr>
<tr>
<th>Parámetros</th>
<td>id: identificador de la publicación a la que se quiere asociar la oferta.</td>
</tr>
<tr>
<th>Encabezados</th>
<td><code>Authorization: Bearer token</code></td>
</tr>
<tr>
<th>Puerto</th>
<td>3007</td>
</tr>
<tr>
<th>Cuerpo</th>
<td>

```json
{
    "description": "descripción del paquete a llevar",
    "size": "LARGE ó MEDIUM ó SMALL",
    "fragile" : "booleano que indica si es un paquete delicado o no",
    "offer": "valor en dólares de la oferta para llevar el paquete"
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
<td>404</td>
<td>La publicación a la que se quiere asociar la oferta no existe.</td>
<td>N/A</td>
</tr>
<tr>
<td>412</td>
<td>La publicación es del mismo usuario y no se puede ofertar por ella.</td>
<td>N/A</td>
</tr>
<tr>
<td>412</td>
<td>La publicación ya está expirada y no se reciben más ofertas por ella.</td>
<td>N/A</td>
</tr>
<tr>
<td>200</td>
<td>Si la creación de la oferta es exitosa. La utilidad de la oferta queda almacenada en la base de datos del servicio de utilidad.</td>
<td>

```json
{
    "data": {
       "id": "id de la oferta",
       "userId": "id del usuario dueño de la oferta",
       "createdAt": "fecha de creación de la oferta",
       "postId": "id de la publicación"
    },
    "msg": "Resumen de la operación *."
}
```

</td>
</tr>
</table>