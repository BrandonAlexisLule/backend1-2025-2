import os
import csv
import sqlite3
from flask import Flask, request, jsonify

#Configuración de la API
app = Flask(__name__)

DB_NAME = "dbinegi.db" #Variable para nombre de base de datos
TABLE_NAME = "No_existe" #Variable para nombre de tabla
CSV_FILE = "denue_inegi.csv"  # Archivo de respaldo externo

#Columnas esperadas dentro del CSV
CSV_COLUMNS = {
    "id": "id",
    "nom_estab": "nom_estab",
    "municipio": "municipio",
    "codigo_act": "codigo_act",
    "nombre_act": "nombre_act",
    "latitud": "latitud",
    "longitud": "longitud",
}

#Creamos los endpoints 
def obtener_conexion():
    """Abre la conexión con SQLite. Si falla, regresa None para levantar el respaldo de CSV."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error:
        return None

def leer_desde_csv(municipio, actividad, limite=500):
    """Busca registros en el archivo CSV cuando no hay conexión SQLite."""
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
                    if contador >= limite:
                        break
                    
        return resultados, None
    except Exception as error:
        return None, str(error)

def buscar_detalle_csv(id_empresa):
    """Busca un registro específico por ID dentro del CSV."""
    if not os.path.exists(CSV_FILE):
        return None, "No se encontró el archivo CSV."
    try:
        with open(CSV_FILE, encoding="utf-8", mode="r") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila.get(CSV_COLUMNS["id"]) == str(id_empresa):
                    return fila, None
        return None, None
    except Exception as error:
        return None, str(error)

# Endpoints
@app.route("/api/empresas", methods=["GET"])
def buscar_empresas(): 
    """Busca establecimientos según municipio y actividad."""
    municipio = request.args.get("municipio")
    actividad = request.args.get("id_actividad")
    query = f"""SELECT id, nom_estab, municipio, codigo_act, nombre_act, latitud, longitud
        FROM {TABLE_NAME} WHERE 1=1"""

    parametros = []
    if municipio:
        query += " AND municipio LIKE ?"
        parametros.append(f"%{municipio}%")
    if actividad:
        query += " AND codigo_act = ?"
        parametros.append(actividad)
    query += " LIMIT 500"
    conexion = obtener_conexion()

    #Si no hay conexión, se cierra el servidor para abrir el servidor de respaldo.
    if conexion is not None:
        try:
            print('SQLite OK')
            filas = conexion.execute(query, parametros).fetchall()
            conexion.close()
            if not filas:
                return jsonify({"mensaje": "No se encontraron resultados."}), 404
            return jsonify([dict(fila) for fila in filas]), 200

        except sqlite3.Error as error:
            conexion.close()
            # Sigue al fallback CSV

    # Fallback: CSV
    resultados, error_csv = leer_desde_csv(municipio, actividad)
    if error_csv:
        return jsonify({
            "error": "No se pudo obtener información ni desde SQLite ni desde el CSV.",
            "detalle": error_csv
        }), 500

    if not resultados:
        return jsonify({"mensaje": "No se encontraron resultados en el archivo de respaldo."}), 404

    return jsonify(resultados), 200

@app.route("/api/empresas/<int:id_empresa>", methods=["GET"])
def detalle_empresa(id_empresa):
    """Devuelve el detalle de una empresa por su ID."""
    conexion = obtener_conexion()

    # Intento principal con SQLite
    if conexion is not None:
        try:
            query = f"SELECT * FROM {TABLE_NAME} WHERE id = ?"
            fila = conexion.execute(query, (id_empresa,)).fetchone()
            conexion.close()
            if fila is None:
                return jsonify({"mensaje": "No existe una empresa con ese ID."}), 404
            return jsonify(dict(fila)), 200

        except sqlite3.Error:
            conexion.close()
            # sigue al respaldo del archivo por comas

    # Respaldo por excel mediante archivo por comas
    fila_csv, error_csv = buscar_detalle_csv(id_empresa)

    if error_csv:
        return jsonify({
            "error": "Error crítico al consultar SQLite y CSV.",
            "detalle": error_csv}), 500

    if fila_csv is None:
        return jsonify({"mensaje": "No existe una empresa con ese ID en el archivo de respaldo."}), 404
    return jsonify(fila_csv), 200

#Inicializar servidor
if __name__ == "__main__":
    app.run(debug=True)
