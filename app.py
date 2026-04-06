import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go


st.set_page_config(page_title="Fraud Detection", page_icon="💳", layout="wide")


@st.cache_resource
def load_objects():
    model = joblib.load("artifacts/model.pkl")
    preprocessor = joblib.load("artifacts/preprocessor.pkl")
    return model, preprocessor

model, preprocessor = load_objects()

st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: bold;
    color: #1f77b4;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f1f5f9;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">💳 Fraud Detection Dashboard</div>', unsafe_allow_html=True)


st.sidebar.header("Transaction Details")

amount = st.sidebar.number_input("Amount", 0.0, 100000.0, 100.0)
transaction_hour = st.sidebar.slider("Hour", 0, 23, 12)
foreign_transaction = st.sidebar.selectbox("Foreign", [0, 1])
location_mismatch = st.sidebar.selectbox("Location Mismatch", [0, 1])
device_trust_score = st.sidebar.slider("Device Trust", 0.0, 1.0, 0.8)
velocity_last_24h = st.sidebar.number_input("Transactions (24h)", 0, 100, 5)
cardholder_age = st.sidebar.slider("Age", 18, 90, 30)
merchant_category = st.sidebar.selectbox(
    "Category",
    ["grocery", "electronics", "fashion", "travel", "others"]
)


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


if st.sidebar.button("🔍 Predict"):

    input_transformed = preprocessor.transform(input_data)

    pred = model.predict(input_transformed)[0]

    try:
        prob = model.predict_proba(input_transformed)[0][1]
    except:
        prob = 0.5


    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="card"><h4>💰 Amount</h4><h2>{amount}</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="card"><h4>📊 Risk</h4><h2>{round(prob*100,2)}%</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="card"><h4>📱 Trust</h4><h2>{device_trust_score}</h2></div>', unsafe_allow_html=True)

    st.write("")


    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={'text': "Fraud Probability"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)
    

    if pred == 1:
        st.error(" Fraud Detected")
    else:
        st.success(" Legit Transaction")