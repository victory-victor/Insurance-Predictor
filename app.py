import streamlit as st
import requests

st.title("Insurance Premium Prediction")

# User inputs
age = st.number_input("Age", min_value=0, max_value=120, value=30)
bmi = st.number_input("BMI", min_value=0.0, max_value=100.0, value=25.0)
children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
sex = st.selectbox("Sex", ["male", "female"])
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["northwest", "northeast", "southeast", "southwest"])

if st.button("Predict"):
    data = {
        "age": age,
        "bmi": bmi,
        "children": children,
        "sex": sex,
        "smoker": smoker,
        "region": region
    }

    # Send POST request to FastAPI
    response = requests.post("http://localhost:8000/predict", json=data)

    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"Estimated Insurance Premium: ${prediction:,.2f}")
    else:
        st.error("Error in prediction")
