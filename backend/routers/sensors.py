from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SensorReading, Alert, get_db
from models.schemas import SensorDataCreate, SensorDataResponse

router = APIRouter(prefix="/sensor-data", tags=["sensors"])

THRESHOLDS = {
    "temperature": {"warning": 75.0, "critical": 90.0},
    "pressure":    {"warning": 8.0,  "critical": 10.0},
    "rpm":         {"warning": 3000, "critical": 3500},
}


def check_and_create_alerts(data: SensorDataCreate, db: Session):
    checks = [
        ("temperature", data.temperature),
        ("pressure", data.pressure),
        ("rpm", data.rpm),
    ]
    for metric, value in checks:
        if value >= THRESHOLDS[metric]["critical"]:
            alert = Alert(
                device_id=data.device_id,
                message=f"{metric} critical: {value}",
                severity="critical"
            )
            db.add(alert)
        elif value >= THRESHOLDS[metric]["warning"]:
            alert = Alert(
                device_id=data.device_id,
                message=f"{metric} warning: {value}",
                severity="warning"
            )
            db.add(alert)
    db.commit()


@router.post("/", response_model=SensorDataResponse)
def receive_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    reading = SensorReading(**data.model_dump())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    check_and_create_alerts(data, db)
    return reading


@router.get("/{device_id}", response_model=list[SensorDataResponse])
def get_sensor_data(device_id: int, limit: int = 50, db: Session = Depends(get_db)):
    return (db.query(SensorReading)
              .filter(SensorReading.device_id == device_id)
              .order_by(SensorReading.timestamp.desc())
              .limit(limit)
              .all())