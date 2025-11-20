from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/malaga', methods=['GET'])
def datos_basicos():
    try:
        with open('../servicio_basico/schema_municipio.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        response_schema = {
            "municipioid": datos["municipioid"],
            "gentilicio": datos["gentilicio"],
            "sitioweb": datos["sitio_web"],
            "provincia": datos["provincia"],
        }
        
        return jsonify(response_schema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')