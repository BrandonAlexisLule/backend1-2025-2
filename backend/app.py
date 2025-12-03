import sqlite3
from flask import Flask, request, jsonify

# --- Configuración ---
app = Flask(__name__)
DB_NAME = 'dbinegi.db'
TABLE_NAME = 'denue_inegi'

#Funciones
#Establecer la conexión a la base de datos ...

def get_db_connection():
    """Conecta a la base de datos, y en caso de que falle, regresa"""
    try:
        conn = sqlite3.connect(DB_NAME) #
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error:
        return None

#Creamos los endpoints
@app.route('/api/empresas', methods=['GET'])
def buscar_empresas():
    municipio = request.args.get('municipio')
    id_actividad = request.args.get('id_actividad')

    #Consultar las empresas por el tipo de actividad y el municipio
    query = f"""
    SELECT id, nom_estab, municipio, codigo_act, nombre_act, latitud, longitud 
    FROM {TABLE_NAME}
    WHERE 1=1
    """
    params = []
    if municipio:
        query += " AND municipio LIKE ?"
        params.append(f'%{municipio}%')
    if id_actividad:
        query += " AND codigo_act = ?"
        params.append(id_actividad)
    query += " LIMIT 500"

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500
    try:
        empresas = conn.execute(query, params).fetchall()
        if not empresas:
            return jsonify({"mensaje": "No se encontraron empresas con esos criterios."}), 404
        empresas_list = [dict(empresa) for empresa in empresas]
        return jsonify(empresas_list), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Error interno del servidor en la base de datos", "detalle": str(e)}), 500
    finally:
        conn.close()
        
@app.route('/api/empresas/<int:id_empresa>', methods=['GET'])
def get_detalle_empresa(id_empresa):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500
    try:
        #Consultar las empresas por su id
        query = f"SELECT * FROM {TABLE_NAME} WHERE id = ?"
        empresa = conn.execute(query, (id_empresa,)).fetchone()
        if empresa is None:
            return jsonify({"mensaje": f"Empresa con ID {id_empresa} no encontrada."}), 404
        return jsonify(dict(empresa)), 200

    except sqlite3.Error as e:
        return jsonify({"error": "Error interno del servidor en la base de datos", "detalle": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
