import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="PremiumGuard AI", page_icon="🏥", layout="centered")

# Custom CSS for a polished look and fixed hover state
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Button Styling */
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        height: 3.5em;
        width: 100%;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    /* HOVER FIX: Darker blue background, white text */
    div.stButton > button:first-child:hover {
        background-color: #0056b3 !important;
        color: white !important;
        border: none !important;
    }

    /* ACTIVE/CLICKED state */
    div.stButton > button:first-child:active {
        background-color: #004085 !important;
        color: white !important;
    }

    /* Input Card Styling */
    [data-testid="stVerticalBlock"] > div:has(div.stNumberInput) {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Insurance Premium Predictor")
st.markdown("Fill in the details below to receive your personalized insurance quote.")
st.write("")

# Main Input Form
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Profile")
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        sex = st.selectbox("Biological Sex", ["male", "female"])
        children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
        
    with col2:
        st.markdown("### 🧬 Health & Location")
        bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, max_value=100.0, value=25.0, format="%.1f")
        smoker = st.selectbox("Smoker Status", ["no", "yes"])
        region = st.selectbox("Region", ["northwest", "northeast", "southeast", "southwest"])

st.write("") 

# Centering the button slightly
if st.button("Calculate My Premium"):
    data = {
        "age": age, "bmi": bmi, "children": children,
        "sex": sex, "smoker": smoker, "region": region
    }

    with st.spinner('🔄 Analyzing insurance risk factors...'):
        try:
            # Added a timeout so the UI doesn't hang indefinitely
            response = requests.post("http://localhost:8000/predict", json=data, timeout=5)
            
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                
                st.markdown("---")
                st.balloons()
                
                # Big Result Card
                result_container = st.container()
                with result_container:
                    st.success("Analysis Complete!")
                    st.metric(label="Estimated Annual Premium", value=f"${prediction:,.2f}")
                    st.caption("This estimate is based on standard actuarial models. Local taxes may apply.")
            else:
                st.error("⚠️ The prediction server is acting up. Please try again.")
        except:
            st.error("🔌 Connection Error: Is the FastAPI server running on localhost:8000?")