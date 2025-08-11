
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_scrape_endpoint_structure():
    """Test that scrape endpoint returns proper structure"""
    response = client.post("/scrape", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields exist
    assert "success" in data
    assert "items" in data  
    assert "total_found" in data
    assert "source_url" in data
    assert data["source_url"] == "https://example.com"

def test_home_endpoint():
    """Test home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
