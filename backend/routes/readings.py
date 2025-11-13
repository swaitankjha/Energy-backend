from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# in-memory database
latest_reading = None
readings_log = []

def safe_reading(r: dict | None):
    """Return a safe reading object even if r is None or missing fields."""
    if r is None:
        return {
            "voltage": 0,
            "current": 0,
            "power": 0,
            "kwh": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    return {
        "voltage": r.get("voltage", 0),
        "current": r.get("current", 0),
        "power": r.get("power", 0),
        "kwh": r.get("kwh", 0),
        "timestamp": r.get("timestamp", datetime.utcnow().isoformat())
    }

@router.post("/update")
async def update_reading(data: dict):
    global latest_reading, readings_log

    latest_reading = {
        "voltage": data.get("voltage", 0),
        "current": data.get("current", 0),
        "power": data.get("power", 0),
        "kwh": data.get("kwh", 0),
        "timestamp": datetime.utcnow().isoformat()
    }

    readings_log.append(latest_reading)

    # keep last 100 readings only
    readings_log = readings_log[-100:]

    return {"status": "ok", "reading": latest_reading}

@router.get("/latest")
async def get_latest():
    return safe_reading(latest_reading)

@router.get("/")
async def get_all(limit: int = 100):
    return [safe_reading(r) for r in readings_log[-limit:]]
