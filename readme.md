# 💳 Credit Card Fraud Detection System

##  Overview

This project is a **Machine Learning-based Credit Card Fraud Detection System** built to identify fraudulent transactions in real-time.
It uses advanced preprocessing techniques, classification models, and an interactive dashboard to deliver predictions with high accuracy.

---

##  Features

*  Real-time fraud prediction
*  Probability-based risk scoring
*  Machine Learning models (AdaBoost, Random Forest, XGBoost, etc.)
*  Data preprocessing pipeline (Scaling + Encoding)
*  Handles imbalanced data using SMOTE
*  Interactive dashboard using Streamlit
*  Transaction storage using SQLite database
*  Downloadable transaction reports

---

##  Project Structure

```
credict_fruad_prediction/
│
├── artifacts/
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── database.py
│   │
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

##  Machine Learning Pipeline

```
Input Features (8)
        ↓
Preprocessing (Scaling + Encoding)
        ↓
SMOTE (Handle Imbalance)
        ↓
Model Training (AdaBoost / Others)
        ↓
Prediction (Fraud / Legit)
```

---

##  Features Used

### Numerical Features:

* amount
* transaction_hour
* foreign_transaction
* location_mismatch
* device_trust_score
* velocity_last_24h
* cardholder_age

### Categorical Features:

* merchant_category

---

##  Tech Stack

* Python 🐍
* Pandas & NumPy
* Scikit-learn
* XGBoost
* Imbalanced-learn (SMOTE)
* Streamlit (Frontend UI)
* SQLite (Database)
* Plotly (Visualization)

---

## ⚙️ Installation & Setup

### 1️ Clone Repository

```
git clone https://github.com/your-username/credict_fruad_prediction.git
cd credict_fruad_prediction
```

### 2️ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

###  Install Dependencies

```
pip install -r requirements.txt
```

###  Run Application

```
streamlit run app.py
```

---

##  Usage

1. Enter transaction details in the sidebar
2. Click **Predict**
3. View:

   * Fraud Prediction
   * Risk Score
   * Visualization dashboard

---

## 📈 Model Performance

* High accuracy and recall on fraud detection
* Confusion Matrix:

```
[[1969    0]
 [   1   30]]
```

---

##  Deployment

* Deployed using Streamlit Cloud
* Can also be converted to a standalone `.exe` application using PyInstaller

---

##  Future Improvements

*  REST API using FastAPI
*  Cloud database (PostgreSQL / AWS)
*  User authentication system
*  Real-time streaming data pipeline
*  Advanced analytics dashboard

---

##  Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

##  Contact

**naradaladurgaprasad@gmail.com**
 Feel free to connect for collaborations and opportunities

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
