from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# Load model, scaler, and columns
with open("insurance_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

app = FastAPI()

# Define input schema
class InsuranceData(BaseModel):
    age: float
    bmi: float
    children: int
    sex: str       # 'male' or 'female'
    smoker: str    # 'yes' or 'no'
    region: str    # 'northwest', 'southeast', 'southwest', 'northeast'

@app.post("/predict")
def predict_insurance(data: InsuranceData):
    # Convert input to dataframe
    input_dict = data.dict()

    # One-hot encode manually to match training columns
    df = pd.DataFrame(columns=model_columns)
    df.loc[0] = 0  # Initialize with zeros
    
    df['age'] = input_dict['age']
    df['bmi'] = input_dict['bmi']
    df['children'] = input_dict['children']

    # Sex
    if input_dict['sex'].lower() == 'male':
        df['sex_male'] = 1

    # Smoker
    if input_dict['smoker'].lower() == 'yes':
        df['smoker_yes'] = 1

    # Region
    region_col = f"region_{input_dict['region'].lower()}"
    if region_col in df.columns:
        df[region_col] = 1

    # Scale numeric features
    df[['age', 'bmi', 'children']] = scaler.transform(df[['age', 'bmi', 'children']])

    # Prediction
    prediction = model.predict(df)[0]

    return {"prediction": float(prediction)}
