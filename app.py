import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Churn Predictor",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: 700;
    background: linear-gradient(to right, #00F5FF, #A855F7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #CBD5E1;
    margin-bottom: 30px;
}

.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0px 8px 32px rgba(0,0,0,0.35);
}

.result-card {
    text-align: center;
    padding: 30px;
    border-radius: 25px;
    font-size: 30px;
    font-weight: bold;
    animation: fadeIn 1s ease-in;
}

.low-risk {
    background: rgba(34,197,94,0.2);
    border: 2px solid #22c55e;
}

.high-risk {
    background: rgba(239,68,68,0.2);
    border: 2px solid #ef4444;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(20px);}
    to {opacity:1; transform:translateY(0);}
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #06b6d4, #9333ea);
    color: white;
    border-radius: 15px;
    height: 60px;
    font-size: 22px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
import joblib

model = joblib.load("bagga.pkl")
# ---------------- TITLE ----------------
st.markdown("<div class='title'>🚀 AI Customer Churn Predictor</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>Predict whether a customer will churn using futuristic AI</div>",
    unsafe_allow_html=True
)

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure (Months)", 0, 72, 12)

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    monthly = st.slider("Monthly Charges", 0, 150, 70)
    total = st.slider("Total Charges", 0, 10000, 2000)
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ENCODING ----------------
gender = 1 if gender == "Male" else 0
partner = 1 if partner == "Yes" else 0
dependents = 1 if dependents == "Yes" else 0

internet_map = {
    "DSL": 0,
    "Fiber optic": 1,
    "No": 2
}

contract_map = {
    "Month-to-month": 0,
    "One year": 1,
    "Two year": 2
}

# ---------------- PREDICT ----------------
if st.button("✨ Predict Churn Risk"):

    input_data = np.array([[
        gender,
        senior,
        partner,
        dependents,
        tenure,
        monthly,
        total,
        internet_map[internet],
        contract_map[contract]
    ]])

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data)[0][1]
    except:
        probability = 0.5

    st.progress(float(probability))

    if prediction == 1:
        st.markdown(f"""
        <div class='result-card high-risk'>
        ⚠️ HIGH CHURN RISK <br>
        Probability: {probability:.2%}
        </div>
        """, unsafe_allow_html=True)

        st.warning("Retention strategy recommended immediately.")

    else:
        st.markdown(f"""
        <div class='result-card low-risk'>
        ✅ LOW CHURN RISK <br>
        Probability: {(1-probability):.2%}
        </div>
        """, unsafe_allow_html=True)

        st.success("Customer likely to stay 🎉")