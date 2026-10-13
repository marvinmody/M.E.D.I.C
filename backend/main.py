
from flask import Flask, jsonify, request
from database import get_connection, initialize_database

app = Flask(__name__)
initialize_database()


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "project": "MEDIC"
    })


@app.get("/inspections")
def get_inspections():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM inspections ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.post("/inspections")
def create_inspection():
    data = request.get_json(silent=True) or {}
    location = data.get("location")

    if not isinstance(location, str) or not location.strip():
        return jsonify({"error": "location is required"}), 400

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO inspections (location) VALUES (?)",
            (location.strip(),)
        )
        inspection_id = cursor.lastrowid

    return jsonify({
        "id": inspection_id,
        "location": location.strip(),
        "status": "pending"
    }), 201


@app.get("/hazards")
def get_hazards():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM hazards ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.post("/hazards")
def create_hazard():
    data = request.get_json(silent=True) or {}

    required = ("inspection_id", "category", "severity")

    if any(
        data.get(field) is None or data.get(field) == ""
        for field in required
    ):
        return jsonify({
            "error": "inspection_id, category, and severity are required"
        }), 400

    try:
        inspection_id = int(data["inspection_id"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "inspection_id must be an integer"
        }), 400

    if not all(
        isinstance(data[key], str) and data[key].strip()
        for key in ("category", "severity")
    ):
        return jsonify({
            "error": "category and severity must be nonempty strings"
        }), 400

    with get_connection() as connection:
        exists = connection.execute(
            "SELECT 1 FROM inspections WHERE id = ?",
            (inspection_id,)
        ).fetchone()

        if not exists:
            return jsonify({
                "error": "inspection not found"
            }), 404

        cursor = connection.execute(
            """
            INSERT INTO hazards
            (inspection_id, category, severity,
             description, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                inspection_id,
                data["category"].strip(),
                data["severity"].strip(),
                data.get("description", ""),
                data.get("latitude"),
                data.get("longitude")
            )
        )

        hazard_id = cursor.lastrowid

    return jsonify({
        "id": hazard_id,
        "inspection_id": inspection_id
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
