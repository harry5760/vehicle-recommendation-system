# 🚗 Vehicle Recommendation System

An end-to-end Machine Learning based vehicle recommendation system that suggests the best vehicles based on user preferences such as budget, durability, maintenance cost, fuel type, and segment.

## 🔥 Features
- Interactive Streamlit web app
- ML-based ranking using Random Forest
- Filters by budget, durability & maintenance
- Segment and fuel type selection
- Realistic Indian vehicle dataset

## 🧠 Machine Learning
- Model: RandomForestRegressor
- Target: Value for Money Score
- Features:
  - Price
  - Durability Score
  - Maintenance Cost
  - Total Cost of Ownership

## 🛠️ Tech Stack
- Python
- Pandas
- Scikit-learn
- Streamlit
- Joblib

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py