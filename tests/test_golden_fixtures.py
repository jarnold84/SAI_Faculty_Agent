
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fresno_music_golden_fixture():
    """
    Golden test: Fresno State Music Faculty Directory
    This test locks in our successful directory_table extraction.
    If this breaks, it means we've regressed on a working case.
    """
    response = client.post("/scrape", json={
        "url": "https://cah.fresnostate.edu/about/directory/music/index.html"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Core success criteria
    assert data["success"] == True
    assert data["strategy_used"] == "directory_table"
    assert data["total_found"] >= 35  # Allow slight variation
    assert len(data["items"]) >= 35
    
    # Sample item validation
    first_item = data["items"][0]
    assert "name" in first_item
    assert "title" in first_item
    assert "profile_url" in first_item
    assert first_item["profile_url"].startswith("https://cah.fresnostate.edu/about/directory/music/")
    
    print(f"✅ Golden fixture passed: {data['total_found']} items extracted")
