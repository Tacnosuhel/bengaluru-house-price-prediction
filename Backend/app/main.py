from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
import pickle

app=FastAPI()
with open("Backend/model/models.pickle", "rb") as f:
  model = pickle.load(f)

# 1. Load columns
with open("Backend/model/columns.json","r") as f:
  json_data=json.load(f)
  data_columns=json_data['data_columns']
  Total_col=len(data_columns)

@app.get("/")
def start():
  return {"Message":"Server Is Running ..."}

class UserInput(BaseModel):
  total_sqft:float
  bath:float
  bhk:float
  location:str

@app.post("/user")
def user(data:UserInput):
  # Zeros ka array banao
  x=np.zeros(Total_col)
  # 2. Location ko one-hot me set karo
  loc=data.location.strip().lower()
  if loc in data_columns:
    location_index=data_columns.index(loc)
 
  x[0]=data.total_sqft
  x[1]=data.bath
  x[2]=data.bhk
  x[location_index]=1

  predicted=model.predict([x])[0]
  return round(predicted,2)



