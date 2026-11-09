from sqlalchemy.orm import Session

from app.models.employee import Employee


def create_employee(db: Session, data: dict):
    employee = Employee(**data)

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def get_all_employees(db: Session):
    return db.query(Employee).all()


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


def delete_employee(db: Session, employee):
    db.delete(employee)
    db.commit()


def update_employee(db: Session, employee, data: dict):
    for key, value in data.items():
        if value is not None:
            setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee