# California Housing Price Prediction API - MLOps Pipeline

This repository implements an end-to-end Machine Learning Operations (MLOps) workflow for predicting California housing prices using FastAPI, Docker, and GitHub Actions.

## 📌 Case Study Overview
- **Dataset**: California Housing Prices (Kaggle)
- **Problem Type**: Regression
- **Target Variable**: `median_house_value`
- **Features Used**:
  - `longitude`, `latitude`
  - `housing_median_age`
  - `total_rooms`, `total_bedrooms`
  - `population`, `households`
  - `median_income`
  - `ocean_proximity` (Categorical: `<1H OCEAN`, `INLAND`, `ISLAND`, `NEAR BAY`, `NEAR OCEAN`)
- **Trained Model**: Scikit-Learn Pipeline with `SimpleImputer`, `OneHotEncoder`, and `HistGradientBoostingRegressor` saved as `models/model.joblib`.

---

## 🚀 Running Locally

1. **Activate Virtual Environment**:
   ```bash
   venv\Scripts\activate   # Windows
   # or source venv/bin/activate # Linux/Mac
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Interactive Swagger docs are available at: `http://localhost:8000/docs`

4. **Run Unit & Integration Tests**:
   ```bash
   pytest -c pytest.ini tests/
   ```

---

## 🐳 Docker Deployment

1. **Build Docker Image**:
   ```bash
   docker build -t california-housing-api .
   ```

2. **Run Docker Container**:
   ```bash
   docker run -d -p 8000:8000 --name housing-api california-housing-api
   ```

3. **Test the Running Container**:
   - Health check:
     ```bash
     curl http://localhost:8000/health
     ```
   - Make a prediction:
     ```bash
     curl -X POST http://localhost:8000/predict \
       -H "Content-Type: application/json" \
       -d '{
         "longitude": -122.23,
         "latitude": 37.88,
         "housing_median_age": 41.0,
         "total_rooms": 880.0,
         "total_bedrooms": 129.0,
         "population": 322.0,
         "households": 126.0,
         "median_income": 8.3252,
         "ocean_proximity": "NEAR BAY"
       }'
     ```

---

## ⚙️ GitHub Actions CI Pipeline
The CI pipeline (`.github/workflows/ci.yml`) automatically triggers on push and pull requests:
1. Sets up Python 3.10
2. Installs requirements
3. Runs Pytest test suite
4. Builds the Docker container
5. Runs the container and validates live `/health` and `/predict` endpoints
