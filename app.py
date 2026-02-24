from flask import Flask, request, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
DATA_FILE = "temperaturas.json"

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f, indent=2)

@app.route("/temperatura", methods=["POST"])
def recibir_temperatura():
    data = request.get_json()
    if not data or "temperatura_c" not in data:
        return jsonify({"error": "JSON invalido"}), 400
    registro = {
        "temperatura_c": data["temperatura_c"],
        "timestamp": datetime.utcnow().isoformat()
    }
    datos = cargar_datos()
    datos.append(registro)
    guardar_datos(datos)
    print(f"[+] {registro}")
    return jsonify({"ok": True}), 200

@app.route("/datos", methods=["GET"])
def obtener_datos():
    return jsonify(cargar_datos()), 200

@app.route("/limpiar", methods=["DELETE"])
def limpiar():
    guardar_datos([])
    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
