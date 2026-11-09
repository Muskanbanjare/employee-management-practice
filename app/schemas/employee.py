from pydantic import BaseModel, EmailStr, ConfigDict


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    department: str | None = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str

    model_config = ConfigDict(from_attributes=True)