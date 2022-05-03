from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas.vehicles import (
    ManifestCreateUpdateSchema,
    ManifestPassengerSchema,
)
from core.tasks.manifests import (
    create_manifest_,
    depopulate_manifest_,
    populate_manifest_,
    search_manifests_,
    update_manifest_,
)
from core.utils import get_current_user


router = APIRouter(
    prefix="/vehicle_manifests",
    tags=["vehicle_manifests"],
    # responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("/search", status_code=200)
def get_manifest(id: Optional[int] = None, db: Session = Depends(get_db)):
    manifests = search_manifests_(id, db)
    if not manifests:
        raise HTTPException(status_code=400, detail="Not found.")
    return manifests


@router.post("/create", status_code=201)
def add_manifest(data: ManifestCreateUpdateSchema, db: Session = Depends(get_db)):
    manifest = create_manifest_(data, db)
    return manifest


@router.put("/{id}/update", status_code=200)
def update_manifest(
    id: int, data: ManifestCreateUpdateSchema, db: Session = Depends(get_db)
):
    manifest = update_manifest_(id, data, db)
    return {"detail": "Success"}


@router.post("/{id}/populate", status_code=200)
def populate_manifest(
    id: int, data: ManifestPassengerSchema, db: Session = Depends(get_db)
):
    populate_manifest_(id, data, db)
    return {"detail": "Success"}


@router.post("/{id}/depopulate", status_code=200)
def depopulate_manifest(
    id: int, data: ManifestPassengerSchema, db: Session = Depends(get_db)
):
    depopulate_manifest_(id, data, db)
    return {"detail": "Success"}
