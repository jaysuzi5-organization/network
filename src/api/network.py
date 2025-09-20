from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from framework.db import get_db
from models.network import Network, NetworkCreate
from datetime import datetime, UTC

router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """
    Convert a SQLAlchemy ORM model instance into a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: Dictionary containing all column names and their values.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/api/v1/network")
def list_network(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of Network records.

    Args:
        page (int): Page number starting from 1.
        limit (int): Maximum number of records to return per page.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: A list of serialized Network records.
    """
    try:
        offset = (page - 1) * limit
        network_records = db.query(Network).offset(offset).limit(limit).all()
        return [serialize_sqlalchemy_obj(item) for item in network_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/network")
def create_record(
    network_data: NetworkCreate = Body(..., description="Data for the new record"),
    db: Session = Depends(get_db)
):
    """
    Create a new Network record.

    Args:
        network_data (NetworkCreate): Data model for the record to create.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The newly created Network record.
    """
    try:
        data = network_data.model_dump(exclude_unset=True)
        new_record = Network(**data)
        new_record.create_date = datetime.now(UTC)
        new_record.update_date = datetime.now(UTC)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return serialize_sqlalchemy_obj(new_record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/network/{id}")
def get_network_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single Network record by ID.

    Args:
        id (int): The ID of the record.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The matching Network record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Network).filter(Network.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Network with id {id} not found")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/network/{id}")
def update_network_full(
    id: int,
    network_data: NetworkCreate = Body(..., description="Updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Fully update an existing Network record (all fields required).

    Args:
        id (int): The ID of the record to update.
        network_data (NetworkCreate): Updated record data (all fields).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Network record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Network).filter(Network.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Network with id {id} not found")

        data = network_data.model_dump(exclude_unset=False)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/api/v1/network/{id}")
def update_network_partial(
    id: int,
    network_data: NetworkCreate = Body(..., description="Partial updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing Network record (only provided fields are updated).

    Args:
        id (int): The ID of the record to update.
        Network_data (NetworkCreate): Partial updated data.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Network record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Network).filter(Network.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Network with id {id} not found")

        data = network_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/v1/network/{id}")
def delete_network(id: int, db: Session = Depends(get_db)):
    """
    Delete a Network record by ID.

    Args:
        id (int): The ID of the record to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Network).filter(Network.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Network with id {id} not found")

        db.delete(record)
        db.commit()
        return {"detail": f"Network with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
