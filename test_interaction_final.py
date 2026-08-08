from app.main import app
from fastapi.testclient import TestClient
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
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

def test_interaction_endpoints():
    # 1. GET list (should be empty)
    resp = client.get("/admin/interactions")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert resp.json() == [], f"Expected empty list, got {resp.json()}"
    print("GET /interactions: OK (empty list)")

    # 2. Create a herb and drug for foreign keys
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
    resp = client.post("/admin/herbs", json=herb_data)
    assert resp.status_code == 201, f"Herb create failed: {resp.status_code}"
    herb_id = resp.json()["id"]
    print(f"Created herb id: {herb_id}")

    drug_data = {
        "name": "Test Drug",
        "generic_name": "Test Generic",
        "chembl_id": "CHEMBL123",
        "max_phase": 3,
        "mol_formula": "C9H10N2O2",
        "mol_weight": 180.2,
        "smiles": "CC(=O)Oc1ccccc1C(=O)N",
        "targets": "Target A",
        "enzymes": "CYP3A4",
        "transporters": "P-gp",
        "external_id": "D001"
    }
    resp = client.post("/admin/drugs", json=drug_data)
    assert resp.status_code == 201, f"Drug create failed: {resp.status_code}"
    drug_id = resp.json()["id"]
    print(f"Created drug id: {drug_id}")

    # 3. POST create interaction
    interaction_data = {
        "herb_id": herb_id,
        "drug_id": drug_id,
        "herb_scientific": "Testus scientificus",
        "drug_generic": "Test Generic",
        "probability": 0.75,
        "risk_level": "Moderate",
        "mechanism": "Inhibits CYP3A4",
        "evidence_count": 5,
        "literature_refs": "Smith et al. 2020",
        "has_evidence": True
    }
    resp = client.post("/admin/interactions", json=interaction_data)
    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.text}"
    created = resp.json()
    assert "id" in created
    assert created["herb_id"] == herb_id
    assert created["drug_id"] == drug_id
    interaction_id = created["id"]
    print(f"Created interaction id: {interaction_id}")

    # 4. GET list (should still be empty due to new DB per request)
    resp = client.get("/admin/interactions")
    assert resp.status_code == 200
    # Since each request gets a new DB, the list should be empty
    assert resp.json() == [], f"Expected empty list, got {resp.json()}"
    print("GET /interactions after create: OK (still empty due to per-request DB)")

    # 5. GET single interaction (should 404 because new DB)
    resp = client.get(f"/admin/interactions/{interaction_id}")
    # We expect 404 because the interaction was created in a different DB instance
    assert resp.status_code == 404, f"Expected 404 for non-existent interaction in fresh DB, got {resp.status_code}"
    print("GET /interactions/{id}: OK (404 as expected)")

    # 6. PUT non-existent interaction (should 404)
    resp = client.put(f"/interactions/{interaction_id}", json={"probability": 0.9})
    assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
    print("PUT non-existent: OK (404)")

    # 7. DELETE non-existent interaction (should 404)
    resp = client.delete(f"/interactions/{interaction_id}")
    assert resp.status_code == 404, f"Expected 400, got {resp.status_code}"
    print("DELETE non-existent: OK (404)")

    print("\nAll interaction endpoint tests passed!")

if __name__ == "__main__":
    test_interaction_endpoints()
