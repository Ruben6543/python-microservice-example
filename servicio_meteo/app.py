from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJydWJlbjA0MjkxQGNvcnJlby51Z3IuZXMiLCJqdGkiOiI2NWZmY2E0Zi0zNGRlLTRiZWEtOTE3Ni0zMjVmYzBhZWI3NzYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2MjM2Nzc0MiwidXNlcklkIjoiNjVmZmNhNGYtMzRkZS00YmVhLTkxNzYtMzI1ZmMwYWViNzc2Iiwicm9sZSI6IiJ9.X8r88OimpWQXambuoLy97H-pAUgWV86fKPI9YUaJLwM"
CODIGO_MUNICIPIO = "29067"

@app.route('/malaga/meteo', methods=['GET'])
def datos_meteorologicos():
    try:
        url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{CODIGO_MUNICIPIO}"
        headers = {'api_key': AEMET_API_KEY}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": f"No se pudo obtener datos para municipio {CODIGO_MUNICIPIO}"}), 404
        
        data_url = response.json().get('datos')
        if not data_url:
            return jsonify({"error": "No se retornó URL de datos desde AEMET"}), 500
        

        data_response = requests.get(data_url)
        
        if data_response.status_code != 200:
            return jsonify({"error": "No se pudieron obtener los datos meteorológicos"}), 500
            
        datos_aemet = data_response.json()

        prediccion_hoy = extract_weather_data(datos_aemet)
        
        meteo_schema = {
            "municipioid": 29067,
            "temperatura_actual": prediccion_hoy.get('temperatura_actual', 'N/A'),
            "temperaturas": {
                "max": prediccion_hoy.get('max_temp', 'N/A'),
                "min": prediccion_hoy.get('min_temp', 'N/A')
            },
            "humedad": prediccion_hoy.get('humedad', 'N/A'),
            "viento": prediccion_hoy.get('viento', 'N/A'),
            "precipitacion": prediccion_hoy.get('precipitacion', 'N/A'),
            "estadocielo": prediccion_hoy.get('estado_cielo', 'N/A')
        }
        
        return jsonify(meteo_schema)
        
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

def extract_weather_data(datos_aemet):
    try:
        if isinstance(datos_aemet, list) and len(datos_aemet) > 0:
            municipio_data = datos_aemet[0]
        else:
            municipio_data = datos_aemet
            
        prediccion = municipio_data.get('prediccion', {})
        dia_data = None
        if 'dia' in prediccion:
            dias = prediccion['dia']
            if isinstance(dias, list) and len(dias) > 0:
                dia_data = dias[0]  # Primer día (hoy)
        
        max_temp = "N/A"
        min_temp = "N/A"
        if dia_data and 'temperatura' in dia_data:
            temp_data = dia_data['temperatura']
            if isinstance(temp_data, dict):
                max_temp = str(temp_data.get('maxima', 'N/A'))
                min_temp = str(temp_data.get('minima', 'N/A'))
        
        humedad = "N/A"
        if dia_data and 'humedadRelativa' in dia_data:
            humedad_data = dia_data['humedadRelativa']
            if isinstance(humedad_data, dict):
                humedad = f"{humedad_data.get('maxima', 'N/A')}%"
        
        viento = "N/A"
        if dia_data and 'viento' in dia_data:
            viento_data = dia_data['viento'][0] if isinstance(dia_data.get('viento'), list) else {}
            velocidad = viento_data.get('velocidad', 'N/A')
            viento = f"{velocidad} km/h"

        precipitacion = "N/A"
        if dia_data and 'precipitacion' in dia_data:
            precip_data = dia_data['precipitacion']
            precipitacion = f"{precip_data}%"
        
        estado_cielo = "N/A"
        if dia_data and 'estadoCielo' in dia_data:
            cielo_data = dia_data['estadoCielo']
            if isinstance(cielo_data, list) and len(cielo_data) > 0:
                descripcion = cielo_data[0].get('descripcion', 'N/A')
                estado_cielo = descripcion
        
        temp_actual = max_temp if max_temp != 'N/A' else 'N/A'
        
        return {
            'max_temp': max_temp,
            'min_temp': min_temp,
            'temperatura_actual': temp_actual,
            'humedad': humedad,
            'viento': viento,
            'precipitacion': precipitacion,
            'estado_cielo': estado_cielo
        }
        
    except Exception as e:
        return {
            'max_temp': 'N/A',
            'min_temp': 'N/A', 
            'temperatura_actual': 'N/A',
            'humedad': 'N/A',
            'viento': 'N/A',
            'precipitacion': 'N/A',
            'estado_cielo': 'N/A'
        }

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')