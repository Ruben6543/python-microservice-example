
# Implementación de microservicios con Python

A continuación, se detallarán los pasos para la creación y ejecución del proyecto.

Considere que el proyecto consiste en reportes meteorológicos provenientes de la Agencia Estatal de Meteorología (AEMET), el cual ofrece servicios REST que pueden utilizarse en sistemas propios, se considero al municipio de __Málaga__.


Tome en cuenta que se utilizó el sistema operativo Windows.
 
## 1. Requerimientos

### 1.1 Python
Debe tener instalado el lenguaje de programación [Python 3.10](https://www.python.org/downloads/release/python-3100/), considere que dicha versión fue utilizada en el proyecto.

Puede verificar la instalacion de python mediante el siguiente comando:

> ```
> py --version 
> ```

### 1.2 Editor de código
Para el presente proyecto se recomienda la instalación de [Visual Studio Code](https://code.visualstudio.com/download) para el desarrollo y ejecución de la aplicación.


## 2. Preparación y ejecución del Proyecto

Si desea utilizar la herramienta _Docker_, puede continuar desde punto 5.

Es importante mencionar que cada proyecto es independiente, por lo que cada uno cuenta con su respectivo `app.py` y _virtual enviroment_.

### 2.1 Virtual enviroment
Para crear un _virtual enviroment_ ejecute el siguiente comando dentro del directorio del proyecto:

> ```
> py -m venv venv 
> ```

A continuación active el _virtual enviroment_:

> ```
> venv\Scripts\activate
> ```

Finalmente ejecute el proyecto:

> ```
> py app.py
> ```

### 2.2 Librerías
Dentro de cada directorio, podra visualizar un archivo _requeriments.txt_ el cual contiene todos los _pacakges_ requeridos por cada proyecto.

Dentro de cada proyecto, con el virtual enviroment activado (véase el punto 2.1), puede instalar los _packages_ con el siguiente comando:

> ```
> pip install -r requirements.txt
> ```

### 2.3 Schemas
Algunos servicios requieren consultar información local como fuente de datos, por tal motivo se tienen diferentes _schemas_ en formato _json_.


## 3. Documentación
Dentro de la estructura del proyecto, podrá visualizar la existencia de cinco carpetas, cada una consiste en un microservicio diferente. 

A continuación se detallarán cada uno de ellos.


### 3.1 Servicio Básico
El proyecto consiste en un servicio API-Rest, cuya finalidad es devolver datos básicos provenientes desde el archivo _schema_municipio.json_.

Únicamente se cuenta con el siguiente método:

**GET** `http://127.0.0.1:5003/malaga/demo`


El método devuelve la siguiente información:

```json
{
    "alcalde": "Francisco de la Torre",
    "municipioid": 29067,
    "numhabitantes": 578460,
    "partidopolitico": "PP"
}
```

### 3.2 Servicio Demo
En segundo lugar, el proyecto _Demo_ también consiste en un servicio API-Rest, cuya finalidad es devolver datos básicos provenientes desde el archivo _schema_demo.json_.

Únicamente se cuenta con el siguiente método:

**GET** `http://127.0.0.1:5000/malaga`


El método devuelve la siguiente información:

```json
{
    "gentilicio": "malagueño/a",
    "municipioid": 29067,
    "provincia": "Málaga",
    "sitioweb": "https://www.malagacf.com/"
}
```

### 3.3 Servicio Geo
En tercer lugar, el proyecto _Geo_, consiste en un servicio API-Rest, cuya finalidad es devolver datos básicos provenientes desde _opendata_ de _AEMET_ para lo cual se utilizó el _package requests_, es necesario contar con un _API key_ para la obtención de datos.

Únicamente se cuenta con el siguiente método:

**GET** `http://127.0.0.1:5001/malaga/geo`


El método devuelve la siguiente información:
```json
{
    "altitud": 8.0,
    "latitud": 36.72034267,
    "longitud": -4.41997511,
    "municipioid": 29067
}
```

### 3.4 Servicio Meteo
En cuarto lugar, el proyecto _Meteo_, de igual forma, consiste en un servicio API-Rest, cuya finalidad es devolver datos básicos provenientes desde _opendata_ de _AEMET_. Es necesario contar con un _API key_ para la obtención de datos.

Únicamente se cuenta con el siguiente método:

**GET** `http://127.0.0.1:5002/malaga/meteo`


El método devuelve la siguiente información, algunos campos tienen el valor _N/A_ por no existir la información requerida:
```json
{
    "estadocielo": "",
    "humedad": "70%",
    "municipioid": 29067,
    "precipitacion": "N/A",
    "temperatura_actual": "20",
    "temperaturas": {
        "max": "20",
        "min": "9"
    },
    "viento": "0 km/h"
}
```

### 3.5 Servicio Combinado
Finalmente, el proyecto _combinado_, es un servicio API-Rest, cuya finalidad es devolver datos básicos provenientes desde _opendata_ de _AEMET_. Es necesario contar con un _API key_ para la obtención de datos.

Únicamente se cuenta con el siguiente método:

**GET** `http://127.0.0.1:5002/malaga//malaga/<tipo1>/<tipo2>`

Considere que los tipos, representan a los servicios mencionados anteriormente, para asi ejecutarlo simultaneamente, estos son: 
- Geo
- Demo
- Meteo

El método devuelve información conforme a los tipos enviados, en este caso _geo_ y _meteo_:
```json
{
    "geo": {
        "altitud": 8.0,
        "latitud": 36.72034267,
        "longitud": -4.41997511,
        "municipioid": 29067
    },
    "meteo": {
        "estadocielo": "",
        "humedad": "70%",
        "municipioid": 29067,
        "precipitacion": "N/A",
        "temperatura_actual": "20",
        "temperaturas": {
            "max": "20",
            "min": "9"
        },
        "viento": "0 km/h"
    }
}
```


## 4. Consideraciones adicionales
 
1. Es posible que un servicio de AEMET no se ejecute correctamente, dado que existe un número limitado de peticiones (error 429), si es el caso, el servicio devolverá un mensaje correspondiente.

2. Se compartió el API key en el código con la finalidad de poder realizar pruebas.

## 5. Docker
Los contenedores _Docker_ permiten desplegar y empaquetar aplicaciones dentro de contenedores, al mismo tiempo permite gestionar estos. Tome en cuenta que no será necesaria la utilización de los entornos virtuales (véase el punto 2.1) si decide ejecutar el proyecto con _docker_.

Para ejecutar el archivo _docker-compose.yml_ en el mismo directorio, ejecute el siguiente comando:

> ```
> docker-compose up --build
> ```

El mismo ejecutara todos los _Dockerfile_ dentro de cada proyecto.

Así mismo, puede ejecutar la compilación y creación de contenedores de manera separada mediante los comandos:

Para su construccion:
> ```
> docker-compose build
> ```


Para su ejecución:
> ```
> docker-compose up
> ```



# Extra

Para visualizar el archivo README.md en VS Code instale la extension _Markdown Preview Enhanced_ y dentro del archivo a visualizar utilice:   

cntrl + shift + v

