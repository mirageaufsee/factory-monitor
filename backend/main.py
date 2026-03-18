from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import init_db
from routers import devices, sensors, alerts

app = FastAPI(title="Factory Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "message": "Factory Monitor is running"}

app.include_router(devices.router)
app.include_router(sensors.router)
app.include_router(alerts.router)