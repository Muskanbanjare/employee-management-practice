from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import employee as repo


def create_employee(db: Session, data: dict):
    return repo.create_employee(db, data)


def get_employees(db: Session):
    return repo.get_all_employees(db)


def get_employee_by_id(db: Session, employee_id: int):
    employee = repo.get_employee(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


def delete_employee(db: Session, employee_id: int):
    employee = get_employee_by_id(db, employee_id)

    repo.delete_employee(db, employee)

    return {"message": "Employee deleted successfully"}

def update_employee(db: Session, employee_id: int, data: dict):
    employee = get_employee_by_id(db, employee_id)

    return repo.update_employee(db, employee, data)