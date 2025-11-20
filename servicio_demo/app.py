from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/malaga/demo', methods=['GET'])
def datos_demograficos():
    try:
        with open('../servicio_demo/schema_demo.json', 'r', encoding='utf-8') as f:
            demo_data = json.load(f)
        
        return jsonify(demo_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "service": "demo"})

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')