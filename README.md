PROJECT WORKFLOW

             PROJECT
                │
        ┌───────┴────────┐
        │                │
    FRONTEND          BACKEND
        │                │
 index.html          FastAPI
        │                │
     Leaflet          APIs
        │                │
        └───────┬────────┘
                │
              DATA
                │
           sites.json

Open the application

When you open:

http://127.0.0.1:8001/
the request goes:

Browser
   │
   ▼
FastAPI
   │
   ├── serves static/index.html
   │
   └── /api/sites
           │
           ▼
       sites.json
           │
           ▼
       Nominatim
           │
           ▼
      coordinates
           │
           ▼
       Leaflet map
The application has to be started through FastAPI.

Sample Demo:

. Start the application
cd C:\Users\12037\Downloads\dispatch-energy-assessment\backend

.\.venv\Scripts\Activate.ps1

uvicorn app.main:app --reload --port 8001

Then open:

http://127.0.0.1:8001/


2. Landing page

Dispatch Energy

[ MAP ]

       📍
                📍

             📍     📍


Sites
--------------------------------
Site 1
Site 2
Site 3
Site 4
Site 5

The four resolved sites appear as map markers.

If the fifth site is intentionally invalid/unresolved, it should appear in the Sites section but won't have a map marker because there are no valid coordinates to plot.

3. Click a marker/site

Clicking a marker should show the site information.

For example:

Site Name

RESOLVED

Address:
123 Example Street, ...

Coordinates:
38.xxxxxx, -77.xxxxxx

Then:

Solar Resource

Average GHI       XXXXX
Average DNI       XXXXX
Tilted Irradiance XXXXX

Then:

PVWatts Estimate

System Capacity
10 kW

Annual Energy
XXXXX kWh

Capacity Factor
XX%

That demonstrates the entire flow:

Address
   ↓
Geocoding
   ↓
Latitude / Longitude
   ↓
Solar Resource
   ↓
PVWatts
   ↓
Energy Estimate
