import sys 
import sklearn.linear_model._logistic as logistic
sys.modules['sklearn.linear_model.logistic'] = logistic
import pickle
import pandas as pd
import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from typing import List


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictRequest(BaseModel):
    inputs_df:List[IrisInput]

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

with open("model.pkl","rb") as f:
    model=pickle.load(f)

@app.post("/predict")
async def predict(body:PredictRequest):
    try:
        rows=[row.model_dump() for row in body.inputs_df]
        df=pd.DataFrame(rows)
        df.columns = [
            "sepal length",
            "sepal width",
            "petal length",
            "petal width",
        ]
        prediction=model.predict(df)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)