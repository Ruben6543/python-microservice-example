from flask import Flask, jsonify
import requests

app = Flask(__name__)

AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJydWJlbjA0MjkxQGNvcnJlby51Z3IuZXMiLCJqdGkiOiI2NWZmY2E0Zi0zNGRlLTRiZWEtOTE3Ni0zMjVmYzBhZWI3NzYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2MjM2Nzc0MiwidXNlcklkIjoiNjVmZmNhNGYtMzRkZS00YmVhLTkxNzYtMzI1ZmMwYWViNzc2Iiwicm9sZSI6IiJ9.X8r88OimpWQXambuoLy97H-pAUgWV86fKPI9YUaJLwM"
CODIGO_MUNICIPIO = "id29067"

@app.route('/malaga/geo', methods=['GET'])
def datos_geograficos():
    try:
        url = f"https://opendata.aemet.es/opendata/api/maestro/municipio/{CODIGO_MUNICIPIO}"
        headers = {'api_key': AEMET_API_KEY}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            return jsonify({
                "error": f"Request limit or throughput per minute exceeded for this user. Please wait until the next minute."
            }), 404
        
        elif response.status_code != 200:
            return jsonify({
                "error": f"Could not fetch data for municipality {CODIGO_MUNICIPIO}"
            }), 404
        
        data_url = response.json().get('datos')
        if not data_url:
            return jsonify({"error": "No data URL returned from AEMET"}), 500
        
        data_response = requests.get(data_url)
        
        if data_response.status_code != 200:
            return jsonify({"error": "Could not fetch geographic data"}), 500

        municipios_data = data_response.json()

        malaga_data = None
        for item in municipios_data:
            if item.get('id') == CODIGO_MUNICIPIO:
                malaga_data = item
                break
        
        if not malaga_data:
            return jsonify({"error": f"Municipality {CODIGO_MUNICIPIO} not found in data"}), 404
        
        geo_schema = {
            "municipioid": 29067,
            "latitud": float(malaga_data.get("latitud_dec")),
            "longitud": float(malaga_data.get("longitud_dec")),
            "altitud": float(malaga_data.get("altitud"))
        }
        
        return jsonify(geo_schema)
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')