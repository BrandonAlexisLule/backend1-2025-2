import sqlite3
import os
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

#Configuración de la API
app = Flask(__name__)
CORS(app)

DB_NAME = "dbinegi.db"
TABLE_NAME = "denue_inegi"
CSV_FILE = "denue_inegi.csv"

CSV_COLUMNS = {
    "id": "id",
    "nom_estab": "nom_estab",
    "municipio": "municipio",
    "codigo_act": "codigo_act",
    "nombre_act": "nombre_act",
    "latitud": "latitud",
    "longitud": "longitud",
}

def obtener_conexion():
    if not os.path.exists(DB_NAME):
        print("SQLite no encontrado, usando respaldo CSV")
        return None
    try:
        conexion = sqlite3.connect(DB_NAME)
        conexion.row_factory = sqlite3.Row
        print("SQLite: Trabajando realmente con SQLite")
        return conexion
    except sqlite3.Error:
        return None

def leer_desde_csv(municipio, actividad, limite=1500):
    if not os.path.exists(CSV_FILE):
        return None, "No se encontró el archivo de respaldo."
    resultados = []
    contador = 0

    try:
        with open(CSV_FILE, encoding="utf-8", mode="r") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                coincide_municipio = True
                coincide_actividad = True

                if municipio:
                    texto = fila.get(CSV_COLUMNS["municipio"], "").lower()
                    if municipio.lower() not in texto:
                        coincide_municipio = False
                if actividad:
                    if fila.get(CSV_COLUMNS["codigo_act"]) != actividad:
                        coincide_actividad = False

                if coincide_municipio and coincide_actividad:
                    resultados.append({
                        "id": fila.get(CSV_COLUMNS["id"]),
                        "nom_estab": fila.get(CSV_COLUMNS["nom_estab"]),
                        "municipio": fila.get(CSV_COLUMNS["municipio"]),
                        "codigo_act": fila.get(CSV_COLUMNS["codigo_act"]),
                        "nombre_act": fila.get(CSV_COLUMNS["nombre_act"]),
                        "latitud": float(fila.get(CSV_COLUMNS["latitud"], 0)),
                        "longitud": float(fila.get(CSV_COLUMNS["longitud"], 0)),
                    })

                    contador += 1
                    if limite and contador >= limite:
                        break

        return resultados, None
    except Exception as error:
        return None, str(error)

@app.route("/")
def inicio():
    return jsonify({
        "Estado": "Probando la API",
        "Probar": [
            "http://localhost:5000/denue_inegi/consultarEmpresas",
        ]
    })

@app.route("/denue_inegi/consultarEmpresas", methods=["GET"])
def buscar_empresas(): 
    municipio = request.args.get("municipio")
    actividad = request.args.get("id_actividad")

    query = f"""
    SELECT id, nom_estab, municipio, codigo_act, nombre_act, latitud, longitud 
    FROM {TABLE_NAME} 
    WHERE 1=1
    LIMIT 1500
    """

    parametros = []
    conexion = obtener_conexion()

    if conexion is not None:
        try:
            print('Servidor usando SQLite')

            filtro = " WHERE 1=1 "
            if municipio:
                filtro += " AND municipio LIKE ?"
                parametros.append(f"%{municipio}%")
            if actividad:
                filtro += " AND codigo_act = ?"
                parametros.append(actividad)

            query = f"""
            SELECT id, nom_estab, municipio, codigo_act, nombre_act, latitud, longitud 
            FROM {TABLE_NAME}
            {filtro}
            LIMIT 1500
            """

            filas = conexion.execute(query, parametros).fetchall()
            conexion.close()

            return jsonify([dict(fila) for fila in filas]), 200

        except sqlite3.Error as error:
            print(error)
            conexion.close()

    resultados, error_csv = leer_desde_csv(municipio, actividad, limite=1500)
    if error_csv:
        return jsonify({"error": error_csv}), 500

    return jsonify(resultados), 200

if __name__ == "__main__":
    app.run(debug=True)
