from typing import Dict
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home() -> Dict:
    return {"Hello": "World"}