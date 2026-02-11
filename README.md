# ChurnRadar 📊

A customer intelligence web app that segments e-commerce customers using **KMeans Clustering** and predicts churn risk using **XGBoost**.

Built with Streamlit for a clean, interactive UI.

## What It Does

- **Customer Segmentation (KMeans)** — Groups customers into 7 behavioral segments (Champions, Power Buyers, Loyal Active, etc.) based on purchase patterns
- **Churn Prediction (XGBoost)** — Predicts how likely a customer is to churn based on their profile
- **Actionable Insights** — Recommends engagement strategies for each segment

## How It Works

1. Enter a customer profile (purchase recency, order count, spending, demographics)
2. Click "Analyze Customer"
3. Get the customer's segment + churn risk + recommended action

## Tech Stack

- **Python**
- **Streamlit** — Frontend
- **scikit-learn** — KMeans clustering, StandardScaler, preprocessing
- **XGBoost** — Churn prediction model
- **pandas / numpy** — Data processing
- **joblib** — Model serialization

## Project Structure

```
├── app.py                  # Streamlit app
├── 1.ipynb                 # Model training notebook
├── segment_model.pkl       # Trained KMeans-based segment classifier
├── churn_model.pkl         # Trained XGBoost churn predictor
├── scaler.pkl              # StandardScaler for feature scaling
├── ecommerce_customer_churn_10k.csv  # Dataset
└── requirements.txt        # Dependencies
```

## Models

### KMeans Clustering
- Trained on 10,000 customer records
- Used Elbow Method to determine optimal k=7
- Features scaled with StandardScaler before clustering
- Segments identified through cluster analysis of recency, frequency, and monetary metrics

### XGBoost Classifier
- Binary classification (churned vs active)
- Trained on label-encoded categorical features
- ~98% accuracy on test set

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

`ecommerce_customer_churn_10k.csv` — 10,000 synthetic e-commerce customer records with features like purchase history, demographics, and churn status.
