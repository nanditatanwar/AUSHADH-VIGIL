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

def test_interaction_crud():
    # First, create a herb
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
    assert resp.status_code == 201
    herb = resp.json()
    herb_id = herb["id"]
    print(f"Created herb id: {herb_id}")

    # Create a drug
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
    assert resp.status_code == 201
    drug = resp.json()
    drug_id = drug["id"]
    print(f"Created drug id: {drug_id}")

    # 1. Get all interactions (should be empty)
    resp = client.get("/admin/interactions")
    assert resp.status_code == 200
    assert resp.json() == []
    print("Initial interaction list empty")

    # 2. Create an interaction
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
    print(f"Create interaction response: {resp.status_code}, {resp.text}")
    assert resp.status_code == 201
    interaction = resp.json()
    interaction_id = interaction["id"]
    assert interaction["herb_id"] == herb_id
    assert interaction["drug_id"] == drug_id
    print(f"Created interaction id: {interaction_id}")

    # 3. Get all interactions (should have one)
    resp = client.get("/admin/interactions")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == interaction_id
    print("Interaction list has one item")

    # 4. Get single interaction
    resp = client.get(f"/admin/interactions/{interaction_id}")
    print(f"Get single interaction: {resp.status_code}, {resp.text}")
    assert resp.status_code == 200
    fetched = resp.json()
    assert fetched["id"] == interaction_id
    assert fetched["herb_id"] == herb_id
    assert fetched["drug_id"] == drug_id
    print("Retrieved single interaction successfully")

    # 5. Update interaction
    update_data = {
        "probability": 0.9,
        "risk_level": "High",
        "mechanism": "Strong inhibition"
    }
    resp = client.put(f"/admin/interactions/{interaction_id}", json=update_data)
    print(f"Update interaction: {resp.status_code}, {resp.text}")
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["id"] == interaction_id
    assert updated["probability"] == 0.9
    assert updated["risk_level"] == "High"
    assert updated["mechanism"] == "Strong inhibition"
    # unchanged fields should remain
    assert updated["herb_id"] == herb_id
    assert updated["drug_id"] == drug_id
    print("Interaction updated successfully")

    # 6. Delete interaction
    resp = client.delete(f"/admin/interactions/{interaction_id}")
    print(f"Delete interaction: {resp.status_code}, {resp.text}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Interaction deleted successfully"

    # 7. Verify deletion
    resp = client.get(f"/admin/interactions/{interaction_id}")
    assert resp.status_code == 404
    print("Interaction deleted and not found")

    # 8. List after deletion should be empty
    resp = client.get("/admin/interactions")
    assert resp.status_code == 200
    assert resp.json() == []
    print("Interaction list empty after deletion")

    print("All interaction tests passed!")

if __name__ == "__main__":
    test_interaction_crud()
