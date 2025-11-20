from flask import Flask, jsonify
import requests

app = Flask(__name__)

SERVICIOS = {
    "geo": "http://127.0.0.1:5001/malaga/geo",
    "meteo": "http://127.0.0.1:5002/malaga/meteo", 
    "demo": "http://127.0.0.1:5003/malaga/demo"
}

@app.route('/malaga/<tipo1>/<tipo2>', methods=['GET'])
def datos_combinados(tipo1, tipo2):
    """Microservicio 5: Combinación de dos servicios"""
    try:
        tipos_validos = ["geo", "meteo", "demo"]
        if tipo1 not in tipos_validos or tipo2 not in tipos_validos:
            return jsonify({"error": "Tipos deben ser: geo, meteo o demo"}), 400
        
        if tipo1 == tipo2:
            return jsonify({"error": "Los tipos deben ser diferentes"}), 400
        
        datos_combinados = {}
        
        try:
            respuesta1 = requests.get(SERVICIOS[tipo1], timeout=5)
            if respuesta1.status_code == 200:
                datos_combinados[tipo1] = respuesta1.json()
            else:
                datos_combinados[tipo1] = {"error": f"Servicio {tipo1} no disponible"}
        except requests.exceptions.RequestException:
            datos_combinados[tipo1] = {"error": f"Servicio {tipo1} no disponible"}

        try:
            respuesta2 = requests.get(SERVICIOS[tipo2], timeout=5)
            if respuesta2.status_code == 200:
                datos_combinados[tipo2] = respuesta2.json()
            else:
                datos_combinados[tipo2] = {"error": f"Servicio {tipo2} no disponible"}
        except requests.exceptions.RequestException:
            datos_combinados[tipo2] = {"error": f"Servicio {tipo2} no disponible"}
        
        return jsonify(datos_combinados)
        
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')