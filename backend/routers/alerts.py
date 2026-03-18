from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import Alert, get_db
from models.schemas import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertResponse])
def get_alerts(resolved: bool = False, db: Session = Depends(get_db)):
    return (db.query(Alert)
              .filter(Alert.resolved == resolved)
              .order_by(Alert.created_at.desc())
              .all())


@router.patch("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.resolved = True
        db.commit()
    return {"status": "resolved"}