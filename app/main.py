from fastapi import FastAPI

from app.database import Base, engine
from app.models.employee import Employee
from app.routes.employee import router

# Learning project: create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(router)