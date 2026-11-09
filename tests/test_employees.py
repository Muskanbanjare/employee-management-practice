import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
	test_engine = create_engine(
		"sqlite://",
		connect_args={"check_same_thread": False},
		poolclass=StaticPool,
	)
	testing_session_local = sessionmaker(
		autocommit=False,
		autoflush=False,
		bind=test_engine,
	)
	Base.metadata.create_all(bind=test_engine)

	def override_get_db():
		db = testing_session_local()
		try:
			yield db
		finally:
			db.close()

	app.dependency_overrides[get_db] = override_get_db
	with TestClient(app) as test_client:
		yield test_client
	app.dependency_overrides.clear()
	Base.metadata.drop_all(bind=test_engine)
	test_engine.dispose()


def test_health_check(client):
	response = client.get("/health")

	assert response.status_code == 200
	assert response.json() == {"status": "ok"}


def test_employee_crud(client):
	employee_data = {
		"name": "Asha Patel",
		"email": "asha@example.com",
		"department": "Engineering",
	}

	created = client.post("/employees/", json=employee_data)
	assert created.status_code == 201
	employee_id = created.json()["id"]

	assert client.get("/employees/").json() == [created.json()]
	assert client.get(f"/employees/{employee_id}").json() == created.json()

	updated = client.put(
		f"/employees/{employee_id}",
		json={"department": "Product"},
	)
	assert updated.status_code == 200
	assert updated.json()["department"] == "Product"

	deleted = client.delete(f"/employees/{employee_id}")
	assert deleted.status_code == 200
	assert client.get(f"/employees/{employee_id}").status_code == 404
