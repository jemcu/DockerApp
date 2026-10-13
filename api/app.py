import os

import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "bd"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tareas (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    descripcion TEXT NOT NULL,
                    completada BOOLEAN NOT NULL DEFAULT FALSE,
                    creada_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """
            )


def serialize_tarea(tarea):
    tarea["completada"] = bool(tarea["completada"])
    return tarea


@app.get("/api/estado")
def estado():
    return jsonify({"version": "1.1", "estado": "activo"})


@app.get("/api/tareas")
def listar_tareas():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, titulo, descripcion, completada, creada_en "
                "FROM tareas ORDER BY id DESC"
            )
            tareas = cursor.fetchall()
    return jsonify([serialize_tarea(tarea) for tarea in tareas])


@app.post("/api/tareas")
def crear_tarea():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"error": "El cuerpo debe ser un objeto JSON."}), 400

    titulo = datos.get("titulo")
    descripcion = datos.get("descripcion", "")
    if not isinstance(titulo, str) or not titulo.strip():
        return jsonify({"error": "El título es obligatorio."}), 400
    if not isinstance(descripcion, str):
        return jsonify({"error": "La descripción debe ser texto."}), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)",
                (titulo.strip(), descripcion.strip()),
            )
            tarea_id = cursor.lastrowid
            cursor.execute(
                "SELECT id, titulo, descripcion, completada, creada_en "
                "FROM tareas WHERE id = %s",
                (tarea_id,),
            )
            tarea = cursor.fetchone()
    return jsonify(serialize_tarea(tarea)), 201


@app.patch("/api/tareas/<int:tarea_id>")
def actualizar_tarea(tarea_id):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict) or not isinstance(datos.get("completada"), bool):
        return jsonify({"error": "Indica completada como un valor booleano."}), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE tareas SET completada = %s WHERE id = %s",
                (datos["completada"], tarea_id),
            )
            if cursor.rowcount == 0:
                cursor.execute("SELECT id FROM tareas WHERE id = %s", (tarea_id,))
                if cursor.fetchone() is None:
                    return jsonify({"error": "Tarea no encontrada."}), 404
            cursor.execute(
                "SELECT id, titulo, descripcion, completada, creada_en "
                "FROM tareas WHERE id = %s",
                (tarea_id,),
            )
            tarea = cursor.fetchone()
    return jsonify(serialize_tarea(tarea))


@app.delete("/api/tareas/<int:tarea_id>")
def eliminar_tarea(tarea_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "Tarea no encontrada."}), 404
    return jsonify({"mensaje": "Tarea eliminada."})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
