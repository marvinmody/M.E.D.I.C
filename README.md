# M.E.D.I.C

**Monitoring and Early Detection Infrastructure Crafter**

MEDIC is a drone-based inspection project designed to help municipalities identify infrastructure damage before it becomes a larger safety issue. The proposed system uses aerial images and computer vision to detect problems such as potholes, damaged pavement, and deteriorating structures.

## Problem

Infrastructure issues can go unnoticed between routine inspections or until someone reports them. Manual inspections take time, and delayed repairs can increase costs and safety risks.

## Project Goals

- Capture images of roads and other infrastructure using a drone.
- Identify and classify visible hazards.
- Record hazard locations and inspection results.
- Support maintenance planning through organized reports.

## Current Development

This repository contains an initial Python backend and SQLite database. It currently stores inspections and hazard records. Drone integration, automated detection, image storage, and report generation are planned for later development.

## Repository Structure

```text
MEDIC/
├── backend/
│   ├── main.py          # API routes
│   └── database.py      # Database setup and connection
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

## Setup

Requires Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start the backend:

```bash
pip install -r requirements.txt
python backend/main.py
```

The API runs locally at `http://127.0.0.1:5000`. The SQLite database is created automatically in `backend/medic.db`.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Check API status |
| GET | `/inspections` | List inspections |
| POST | `/inspections` | Add an inspection |
| GET | `/hazards` | List hazards |
| POST | `/hazards` | Add a hazard |

Example inspection request:

```bash
curl -X POST http://127.0.0.1:5000/inspections -H "Content-Type: application/json" -d '{"location":"Hoboken, NJ"}'
```

Example hazard request (after inspection 1 exists):

```json
{
  "inspection_id": 1,
  "category": "pothole",
  "severity": "medium",
  "description": "Road surface damage",
  "latitude": 40.7440,
  "longitude": -74.0324
}
```

## Next Steps

Connect drone image capture, integrate a computer vision model, and add reporting tools for municipal users.
