from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas.accounts import Status
from core.models.accounts import User


def search(
    id: Optional[int] = None,
    email: Optional[str] = None,
    status: Optional[Status] = None,
    db: Session = Depends(get_db),
):
    res = None
    if id and not (email and status):
        res = db.query(User).filter(User.id == id).first()
    elif email and not id and not status:
        res = db.query(User).filter(User.email == email).first()
    elif status and not id and not email:
        res = db.query(User).filter(User.status == status).first()
    return res
