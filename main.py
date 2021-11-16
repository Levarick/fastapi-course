#Python
from typing import Dict, Optional
from fastapi.param_functions import Query

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body, Query

app = FastAPI()

#Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home() -> Dict:
    return {"Hello": "World"}

# Request and Response

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validation: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: int = Query(..., ge=18)      
):
    return {name: age}