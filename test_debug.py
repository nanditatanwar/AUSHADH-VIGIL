import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.api.v1.routers.auth import get_current_admin
from app.db.models.user import User

# Override get_db to provide an in-memory SQLite database
async def override_get_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await engine.dispose()

# Override get_current_admin to return a mock superuser
async def override_get_current_admin():
    return User(id=1, username="admin", email="admin@example.com", hashed_password="", is_active=True, is_superuser=True)

# Apply overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_admin] = override_get_current_admin

client = TestClient(app)

def test_admin_herb_crud():
    # GET empty list
    response = client.get("/admin/herbs")
    print(f"GET /admin/herbs -> status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    assert response.json() == []

    # POST create herb
    herb_data = {
        "name": "Test Herb",
        "scientific_name": "Testus scientificus",
        "description": "A test herb",
        "part_used": "Leaf",
        "active_compounds": "Compound X",
        "traditional_uses": "Testing",
        "sanskrit_name": "Testus",
        "category": "Test",
        "source": "Lab",
        "constituents": "Constituent A",
        "external_id": "T001"
    }
    response = client.post("/admin/herbs", json=herb_data)
    print(f"POST /admin/herbs -> status: {response.status_code}, body: {response.text}")
    assert response.status_code == 201
    created = response.json()
    herb_id = created["id"]
    assert created["name"] == herb_data["name"]

    # GET single herb
    response = client.get(f"/admin/herbs/{herb_id}")
    print(f"GET /admin/herbs/{{herb_id}} -> status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["id"] == herb_id
    assert fetched["name"] == herb_data["name"]

    # PUT update herb
    update_data = {"name": "Updated Herb", "description": "Updated description"}
    response = client.put(f"/admin/herbs/{herb_id}", json=update_data)
    print(f"PUT /admin/herbs/{{herb_id}} -> status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == update_data["name"]
    assert updated["description"] == update_data["description"]
    # unchanged fields
    assert updated["scientific_name"] == herb_data["scientific_name"]

    # DELETE herb
    response = client.delete(f"/admin/herbs/{herb_id}")
    print(f"DELETE /admin/herbs/{{herb_id}} -> status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    assert response.json()["message"] == "Herb deleted successfully"

    # Verify deletion
    response = client.get(f"/admin/herbs/{herb_id}")
    print(f"GET /admin/herbs/{{herb_id}} after delete -> status: {response.status_code}, body: {response.text}")
    assert response.status_code == 404

    print("All tests passed!")

if __name__ == "__main__":
    test_admin_herb_crud()
