from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

# Input schema
class InsuranceData(BaseModel):
    age: float
    bmi: float
    children: int
    sex: str
    smoker: str
    region: str

# Load HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=html_content)


@app.post("/predict")
def predict_insurance(data: InsuranceData):
    input_dict = data.dict()
    df = pd.DataFrame(columns=model_columns)
    df.loc[0] = 0
    
    df['age'] = input_dict['age']
    df['bmi'] = input_dict['bmi']
    df['children'] = input_dict['children']

    if input_dict['sex'].lower() == 'male':
        df['sex_male'] = 1
    if input_dict['smoker'].lower() == 'yes':
        df['smoker_yes'] = 1
    region_col = f"region_{input_dict['region'].lower()}"
    if region_col in df.columns:
        df[region_col] = 1

    df[['age', 'bmi', 'children']] = scaler.transform(df[['age', 'bmi', 'children']])
    prediction = model.predict(df)[0]

    return {"prediction": float(prediction)}
