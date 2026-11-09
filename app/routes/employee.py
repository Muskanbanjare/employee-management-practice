from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.services import employee as service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return service.create_employee(
        db, data.model_dump()
    )


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return service.get_employees(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return service.get_employee_by_id(db, employee_id)


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return service.delete_employee(db, employee_id)

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    return service.update_employee(
        db,
        employee_id,
        data.model_dump(exclude_unset=True)
    )