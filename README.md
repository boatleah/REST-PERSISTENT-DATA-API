# REST-PERSISTENT-DATA-API

## Run
    pip install flask sqlalchemy pydantic
    python main.py

## Test 1: POST a record
Command:
```
curl -X POST http://127.0.0.1:8000/clinical/ ^
-H "Content-Type: application/json" ^
-d "{\"patient_name\":\"Alice Doe\",\"age\":35,\"diagnosis\":\"Hyper\",\"blood_pressure\":\"130/85\",\"heart_rate\":78,\"medication\":\"Lisinopril 10mg\"}"
```
Output:
```
{
  "age": 35,
  "blood_pressure": "130/85",
  "diagnosis": "Hyper",
  "heart_rate": 78,
  "id": 3,
  "medication": "Lisinopril 10mg",
  "patient_name": "Alice Doe",
  "recorded_at": "2026-11-04T19:29:36.321631"
}
```

## Test 2: GET all records
Command: 
```
curl http://127.0.0.1:8000/clinical/
```
Output:
```
[
  {
    "age": 35,
    "blood_pressure": "130/85",
    "diagnosis": "Hypertension",
    "heart_rate": 78,
    "id": 1,
    "medication": "Lisinopril 10mg",
    "patient_name": "Alice Doe",
    "recorded_at": "2026-11-04T19:00:49.000326"
  },
  {
    "age": 52,
    "blood_pressure": "125/80",
    "diagnosis": "Diabetes",
    "heart_rate": 70,
    "id": 2,
    "medication": "Metformin 500mg",
    "patient_name": "Bob Smith",
    "recorded_at": "2026-11-04T19:23:37.671781"
  },
  {
    "age": 35,
    "blood_pressure": "130/85",
    "diagnosis": "Hyper",
    "heart_rate": 78,
    "id": 3,
    "medication": "Lisinopril 10mg",
    "patient_name": "Alice Doe",
    "recorded_at": "2026-11-04T19:29:36.321631"
  }
]
```

## Test 3: SQLite3 database
Command: 
```
python -c "import sqlite3; [print(r) for r in sqlite3.connect('clinical_data.db').execute('SELECT * FROM clinical_data')]"
```
Output:
```
(1, 'Alice Doe', 35, 'Hypertension', '2026-11-04 19:00:49.000326', '130/85', 78, 'Lisinopril 10mg')
(2, 'Bob Smith', 52, 'Diabetes', '2026-11-04 19:23:37.671781', '125/80', 70, 'Metformin 500mg')
(3, 'Alice Doe', 35, 'Hyper', '2026-11-04 19:29:36.321631', '130/85', 78, 'Lisinopril 10mg')
```

## Test 4: JSON Lines
Command: 
```
more data\clinical_data.jsonl
```
Output:
```
{"id": 1, "patient_name": "Alice Doe", "age": 35, "diagnosis": "Hypertension", "blood_pressure": "130/85", "heart_rate": 78, "medication": "Lisinopril 10mg", "recorded_at": "2026-11-04T19:00:49.000326"}
{"id": 2, "patient_name": "Bob Smith", "age": 52, "diagnosis": "Diabetes", "blood_pressure": "125/80", "heart_rate": 70, "medication": "Metformin 500mg", "recorded_at": "2026-11-04T19:23:37.671781"}
{"id": 3, "patient_name": "Alice Doe", "age": 35, "diagnosis": "Hyper", "blood_pressure": "130/85", "heart_rate": 78, "medication": "Lisinopril 10mg", "recorded_at": "2026-11-04T19:29:36.321631"}
```
