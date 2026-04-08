import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import time


st.set_page_config(page_title="Fraud Detection", page_icon="💳", layout="wide")

@st.cache_resource
def load_objects():
    model = joblib.load("artifacts/model.pkl")
    preprocessor = joblib.load("artifacts/preprocessor.pkl")
    return model, preprocessor

model, preprocessor = load_objects()

# -----------------------------
# DARK THEME + ANIMATION CSS
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #0f172a;
    color: white;
}

/* Title */
.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #38bdf8;
    animation: fadeIn 1s ease-in;
}

/* Cards */
.card {
    background: rgba(30, 41, 59, 0.8);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 0 15px rgba(56,189,248,0.2);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: scale(1.05);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Pulse for fraud alert */
.pulse {
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0% {box-shadow: 0 0 10px red;}
    50% {box-shadow: 0 0 25px red;}
    100% {box-shadow: 0 0 10px red;}
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown('<div class="title">💳 AI Fraud Detection System</div>', unsafe_allow_html=True)
st.write("")

# -----------------------------
# LAYOUT
# -----------------------------
left, right = st.columns([1, 2])

# -----------------------------
# INPUT PANEL
# -----------------------------
with left:
    st.subheader("🔧 Transaction Input")

    amount = st.number_input("Amount", 0.0, 100000.0, 100.0)
    transaction_hour = st.slider("Hour", 0, 23, 12)
    foreign_transaction = st.selectbox("Foreign", [0, 1])
    location_mismatch = st.selectbox("Location Mismatch", [0, 1])
    device_trust_score = st.slider("Device Trust", 0.0, 1.0, 0.8)
    velocity_last_24h = st.number_input("Transactions (24h)", 0, 100, 5)
    cardholder_age = st.slider("Age", 18, 90, 30)
    merchant_category = st.selectbox(
        "Category",
        ["grocery", "electronics", "fashion", "travel", "others"]
    )

    predict_btn = st.button("🚀 Analyze Transaction")

# -----------------------------
# OUTPUT PANEL
# -----------------------------
with right:

    if predict_btn:

        # Simulate real-time processing
        with st.spinner("Analyzing transaction..."):
            time.sleep(1.5)

        input_data = pd.DataFrame({
            'amount': [amount],
            'transaction_hour': [transaction_hour],
            'foreign_transaction': [foreign_transaction],
            'location_mismatch': [location_mismatch],
            'device_trust_score': [device_trust_score],
            'velocity_last_24h': [velocity_last_24h],
            'cardholder_age': [cardholder_age],
            'merchant_category': [merchant_category]
        })

        input_transformed = preprocessor.transform(input_data)

        pred = model.predict(input_transformed)[0]

        try:
            prob = model.predict_proba(input_transformed)[0][1]
        except:
            prob = 0.5

        # KPI CARDS
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f'<div class="card">💰<h4>Amount</h4><h2>{amount}</h2></div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f'<div class="card">📊<h4>Risk</h4><h2>{round(prob*100,2)}%</h2></div>', unsafe_allow_html=True)

        with c3:
            st.markdown(f'<div class="card">📱<h4>Trust</h4><h2>{device_trust_score}</h2></div>', unsafe_allow_html=True)

        st.write("")

        # GAUGE
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={'text': "Fraud Probability"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#38bdf8"},
                'steps': [
                    {'range': [0, 30], 'color': "#22c55e"},
                    {'range': [30, 70], 'color': "#eab308"},
                    {'range': [70, 100], 'color': "#ef4444"}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        # RESULT
        if pred == 1:
            st.markdown('<div class="pulse">🚨 FRAUD DETECTED</div>', unsafe_allow_html=True)
        else:
            st.success("✅ Legit Transaction") 

import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import time

# -----------------------------
# DATABASE IMPORTS
# -----------------------------
from src.components.databases.database import (
    create_table,
    insert_transaction,
    fetch_transactions,
    get_stats
)

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Fraud Detection", page_icon="💳", layout="wide")

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_objects():
    model = joblib.load("artifacts/model.pkl")
    preprocessor = joblib.load("artifacts/preprocessor.pkl")
    return model, preprocessor

model, preprocessor = load_objects()

# -----------------------------
# INIT DATABASE
# -----------------------------
create_table()

# -----------------------------
# DARK UI STYLE
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}

.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #38bdf8;
}

.card {
    background: rgba(30, 41, 59, 0.9);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💳 AI Fraud Detection Dashboard</div>', unsafe_allow_html=True)
st.write("")

# -----------------------------
# LAYOUT
# -----------------------------
left, right = st.columns([1, 2])

# -----------------------------
# INPUT PANEL
# -----------------------------
with left:
    st.subheader("🔧 Transaction Input")

    amount = st.number_input("Amount", 0.0, 100000.0, 100.0, key="amount")

    transaction_hour = st.slider("Hour", 0, 23, 12, key="hour")

    foreign_transaction = st.selectbox("Foreign", [0, 1], key="foreign")

    location_mismatch = st.selectbox("Location Mismatch", [0, 1], key="location")

    device_trust_score = st.slider("Device Trust", 0.0, 1.0, 0.8, key="trust")

    velocity_last_24h = st.number_input("Transactions (24h)", 0, 100, 5, key="velocity")

    cardholder_age = st.slider("Age", 18, 90, 30, key="age")

    merchant_category = st.selectbox(
        "Category",
        ["grocery", "electronics", "fashion", "travel", "others"],
        key="category"
    )

    predict_btn = st.button("🚀 Analyze Transaction", key="predict_main")

# -----------------------------
# OUTPUT PANEL
# -----------------------------
with right:

    if predict_btn:

        with st.spinner("Analyzing transaction..."):
            time.sleep(1.2)

        input_data = pd.DataFrame({
            'amount': [amount],
            'transaction_hour': [transaction_hour],
            'foreign_transaction': [foreign_transaction],
            'location_mismatch': [location_mismatch],
            'device_trust_score': [device_trust_score],
            'velocity_last_24h': [velocity_last_24h],
            'cardholder_age': [cardholder_age],
            'merchant_category': [merchant_category]
        })

        # TRANSFORM
        input_transformed = preprocessor.transform(input_data)

        # PREDICT
        pred = model.predict(input_transformed)[0]

        try:
            prob = model.predict_proba(input_transformed)[0][1]
        except:
            prob = 0.5

        # SAVE TO DATABASE
        insert_transaction(input_data.iloc[0].to_dict(), pred, prob)

        # KPI CARDS
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f'<div class="card">💰<h4>Amount</h4><h2>{amount}</h2></div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f'<div class="card">📊<h4>Risk</h4><h2>{round(prob*100,2)}%</h2></div>', unsafe_allow_html=True)

        with c3:
            st.markdown(f'<div class="card">📱<h4>Trust</h4><h2>{device_trust_score}</h2></div>', unsafe_allow_html=True)

        st.write("")

        # GAUGE CHART
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={'text': "Fraud Probability"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#38bdf8"},
                'steps': [
                    {'range': [0, 30], 'color': "#22c55e"},
                    {'range': [30, 70], 'color': "#eab308"},
                    {'range': [70, 100], 'color': "#ef4444"}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        # RESULT
        if pred == 1:
            st.error("🚨 Fraud Detected")
        else:
            st.success("✅ Legit Transaction")

# -----------------------------
# 📊 ANALYTICS SECTION
# -----------------------------
st.write("")
st.subheader("📊 Transaction Analytics")

stats = get_stats()

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", stats["total_transactions"])
col2.metric("Fraud Transactions", stats["fraud_transactions"])
col3.metric("Fraud Rate (%)", stats["fraud_rate"])

# -----------------------------
# 📜 HISTORY TABLE
# -----------------------------
st.write("")
st.subheader("📜 Transaction History")

df = fetch_transactions()

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions yet")