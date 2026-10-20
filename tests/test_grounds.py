from fastapi.testclient import TestClient
from groundbook.app import create_app

def test_B01_proves_second_start_does_not_load_the_four_grounds_again():
    """Verifies that executing startup seeding routines multiple times behaves idempotently."""
    # First app startup verification sequence
    app1 = create_app()
    with TestClient(app1) as client1:
        response1 = client1.get("/venues/deccan/grounds")
        assert response1.status_code == 200

    # Second consecutive app startup execution block on the same persistence context
    app2 = create_app()
    with TestClient(app2) as client2:
        response2 = client2.get("/venues/deccan/grounds")
        assert response2.status_code == 200
        data = response2.json()
        
        # Validates that precisely four grounds are maintained
        assert len(data["grounds"]) == 4