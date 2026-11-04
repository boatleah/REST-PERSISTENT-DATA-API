# main.py
import json
from pathlib import Path
from flask import Flask, request, jsonify, g
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import ClinicalData
from schemas import ClinicalDataCreate, ClinicalDataRead

app = Flask(__name__)

# ---------------------------------------------------------------------------
# 1️⃣ Create tables on startup (just like FastAPI's startup event)
# ---------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# 2️⃣ JSON‑Lines file helpers
# ---------------------------------------------------------------------------
DATA_FILE = Path("data/clinical_data.jsonl")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists


def append_to_file(record: dict):
    """Append a single clinical record as a JSON string followed by a newline."""
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# 3️⃣ Session per request -- Flask style
# ---------------------------------------------------------------------------
@app.before_request
def create_session():
    g.db = SessionLocal()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db: Session = getattr(g, "db", None)
    if db is not None:
        db.close()


# ---------------------------------------------------------------------------
# 4️⃣ POST /clinical/ -- Create a new record
# ---------------------------------------------------------------------------
@app.route("/clinical/", methods=["POST"])
def create_record():
    # Validate request body using Pydantic
    try:
        payload = request.get_json(force=True)  # force=True → return {} if no JSON
        clinical_data = ClinicalDataCreate(**payload)
    except Exception as exc:  # includes ValidationError, TypeError, etc.
        return jsonify({"detail": str(exc)}), 400

    db: Session = g.db
    db_item = ClinicalData(
        patient_name=clinical_data.patient_name,
        age=clinical_data.age,
        diagnosis=clinical_data.diagnosis,
        blood_pressure=clinical_data.blood_pressure,
        heart_rate=clinical_data.heart_rate,
        medication=clinical_data.medication,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Write to JSON‑Lines file (ISO‑formatted timestamp)
    file_record = {
        "id": db_item.id,
        "patient_name": db_item.patient_name,
        "age": db_item.age,
        "diagnosis": db_item.diagnosis,
        "blood_pressure": db_item.blood_pressure,
        "heart_rate": db_item.heart_rate,
        "medication": db_item.medication,
        "recorded_at": db_item.recorded_at.isoformat(),
    }
    append_to_file(file_record)

    return jsonify(file_record), 201  # 201 Created


# ---------------------------------------------------------------------------
# 5️⃣ GET /clinical/ -- Retrieve all records
# ---------------------------------------------------------------------------
@app.route("/clinical/", methods=["GET"])
def read_records():
    db: Session = g.db
    records = db.query(ClinicalData).all()
    result = [r.to_dict() for r in records]
    return jsonify(result)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # For development only -- use a production WSGI server (gunicorn, uWSGI) otherwise.
    app.run(host="0.0.0.0", port=8000, debug=True)