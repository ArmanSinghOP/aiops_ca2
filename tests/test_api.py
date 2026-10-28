from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "California Housing Price Prediction API" in data["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict_success():
    payload = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41.0,
        "total_rooms": 880.0,
        "total_bedrooms": 129.0,
        "population": 322.0,
        "households": 126.0,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "predicted_house_value" in data
    assert isinstance(data["predicted_house_value"], (int, float))
    assert data["predicted_house_value"] > 0


def test_predict_default_values():
    response = client.post("/predict", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["predicted_house_value"] > 0


def test_predict_invalid_data():
    response = client.post("/predict", json={"longitude": "invalid_value"})
    assert response.status_code == 422
