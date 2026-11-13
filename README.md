# FlightLane

**YOUR FLIGHT. YOUR FOCUS.**

A free, mobile-first flight focus companion. Choose a focus duration, route and speed, then follow a 2D aircraft on a Leaflet map.

## Prototype features
- Leaflet + OpenStreetMap map
- Global airport search from OurAirports CSV
- Focus duration and 1x / 2x / 4x / 8x / 16x / 32x / 64x speed controls
- Route preview with generated intermediate waypoints
- Animated aircraft marker with heading rotation
- Completed and remaining route lines, distance and ETA estimates
- Flight phases from gate through taxi, takeoff, cruise, landing and taxi-in

## Run
Open a local server from frontend: `python3 -m http.server 8080`, then visit `http://localhost:8080`.

Backend scaffold: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload`.

## Accuracy
This is a visual focus simulation, not operational navigation. OurAirports provides airport records, but public gate, taxiway, runway, SID/STAR and airway coverage varies. Generated waypoints and airport ground sequences must never be represented as verified procedures. Next stage: integrate airport-specific OpenStreetMap surface geometry and properly licensed aviation navigation data, with explicit fallbacks where data is missing. ETA uses estimated speed and route distance, not live weather or ATC.

## Stack
Vanilla HTML/CSS/JS, Leaflet, OpenStreetMap, OurAirports, FastAPI. PostgreSQL and timestamp-based persistence are planned.