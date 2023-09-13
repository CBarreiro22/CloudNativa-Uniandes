# Componente "Scores" - Cálculo del Score en la aplicación


## Descripción

El servicio de score es una parte fundamental de nuestra plataforma que permite calcular la ganancia aproximada sobre una oferta realizada. Esta se calcula de la forma:

> utilidad = monto oferta - (porcentaje de ocupación de una maleta * valor de la maleta en el trayecto)

<ul>
<li><strong>Monto oferta:</strong> valor en dólares de la oferta por llevar el paquete</li>
<li><strong>Porcentaje de ocupación de una maleta:</strong>

<table align="center">
<tr>
<th>
Tamaño del paquete
</th>
<th>Porcentaje ocupación en la maleta</th>
</tr>
<tr align="center">
<td>VOLUMINOSO / LARGE</td>
<td>100%</td>
</tr>
<tr align="center">
<td>MEDIANO / MEDIUM</td>
<td>50%</td>
</tr>
<tr align="center">
<td>PEQUEÑO / SMALL</td>
<td>25%</td>
</tr>
</table>
</li>

<li><strong>Valor de la maleta en el trayecto:</strong>
costo del envío de una maleta en el trayecto
</li>
</ul>

## Despliegue

Para el despliegue de este servicio se va a escuchar por el puerto 3004

### Calculo  del Score
<table>
<tr>
<th>Método</th>
<td>POST</td>
</tr>
<tr>
<th>Ruta</th>
<td>/score</td>
</tr>
<tr>
<th>Parametros</th>
<td>N/A</td>
</tr>
<tr>
<th>Encabezados</th>
<td>N/A</td>
</tr>
<tr>
<th>Cuerpo</th>
<td>

```json
{
  "id_offer":"Id de la oferta",
  "id_route":"Id de la ruta"
}

```

</td>
</tr>
</table>

### Consulta del Score
<table>
<tr>
<th>Método</th>
<td>Get</td>
</tr>
<tr>
<th>Ruta</th>
<td>/score</td>
</tr>
<tr>
<th>Parametros</th>
<td>id_offer: identificador de la oferta</td>
</tr>
<tr>
<th>Encabezados</th>
<td>N/A</td>
</tr>
<tr>
<th>Cuerpo</th>
<td>N/A</td>
</tr>
</table>

## Organizacion
```shell
.
├── Dockerfile
├── README.md
├── requirements.txt
├── src
│   ├── blueprints
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── scoreOperation.cpython-310.pyc
│   │   │   └── user.cpython-310.pyc
│   │   └── scoreOperation.py
│   ├── errors
│   │   ├── errors.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── errors.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-310.pyc
│   │   │   ├── model.cpython-310.pyc
│   │   │   └── score.cpython-310.pyc
│   │   └── score.py
│   └── __pycache__
│       ├── __init__.cpython-310.pyc
│       └── main.cpython-310.pyc
└── tests
    ├── blueprint
    │   ├── __init__.py
    │   └── test_scores.py
    ├── conftest.py
    └── __init__.py

```
g