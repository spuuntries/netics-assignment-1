import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime

# A bit of path shenanigans here, since I kinda need main to be importable
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert "nama" in data
    assert "nrp" in data
    assert "status" in data
    assert "timestamp" in data
    assert "uptime" in data

    assert data["nama"] == "Faiz Muhammad Kautsar"
    assert data["nrp"] == "5054231013"
    assert data["status"] == "UP"

    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")

    print("All tests passed!")
