""""FlightLane API and static frontend server. Not a certified flight planner."""
from datetime import datetime, timezone
from enum import Enum
from math import radians, sin, cos, asin, sqrt
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="FlightLane API", version="0.1.0", description="Free flight-focus companion API; estimates only.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

class Speed(float, Enum):
    x1 = 1
    x2 = 2
    x4 = 4
    x8 = 8
    x16 = 16
    x32 = 32
    x64 = 64

class Coordinate(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)

class FlightCreate(BaseModel):
    origin: str
    destination: str
    origin_position: Coordinate
    destination_position: Coordinate
    speed: Speed = Speed.x1
    aircraft: str = "A320neo"

class FlightSnapshot(BaseModel):
    origin: str
    destination: str
    distance_nm: float
    speed: float
    created_at: datetime
    estimated_simulated_minutes: float
    estimated_wall_minutes: float

def distance_nm(a: Coordinate, b: Coordinate) -> float:
    lat1, lat2 = radians(a.lat), radians(b.lat)
    dlat, dlon = radians(b.lat-a.lat), radians(b.lon-a.lon)
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 3440.065 * 2 * asin(sqrt(h))

@app.get("/health")
def health():
    return {"status": "ok", "service": "flightlane-api"}

@app.post("/api/estimate", response_model=FlightSnapshot)
def estimate(p: FlightCreate):
    nm = distance_nm(p.origin_position, p.destination_position)
    cruise = {"A320neo": 440, "A321neo": 450, "B787": 485}.get(p.aircraft)
    if cruise is None:
        raise HTTPException(status_code=400, detail="Unsupported aircraft")
    mins = max(35.0, nm / cruise * 60 + 35)
    return FlightSnapshot(origin=p.origin, destination=p.destination, distance_nm=round(nm, 1), speed=float(p.speed.value), created_at=datetime.now(timezone.utc), estimated_simulated_minutes=round(mins, 1), estimated_wall_minutes=round(mins / p.speed.value, 1))

# Serve the web app from the same container so Railway needs no separate static service.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
