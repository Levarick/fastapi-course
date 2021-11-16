#Python
from typing import Dict, Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, HttpUrl

#FastAPI
from fastapi import FastAPI 
from fastapi import Body, Query, Path
from pydantic.types import PaymentCardNumber

app = FastAPI()

#Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    age: int = Field(
        ...,
        gt = 0,
        le = 115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Facundo",
                "last_name": "Garcia Martoni",
                "age": 21,
                "hair_color": "blonde",
                "is_married": False
            }
        }

class Developer(Person):
    
    email: EmailStr = Field(
        ...
    )
    site: HttpUrl = Field(
        ...
    )
    payment_card: PaymentCardNumber = Field(
        ...
    )
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Facundo",
                "last_name": "Garcia Martoni",
                "age": 21,
                "hair_color": "blonde",
                "is_married": False,
                "email": "user@example.com",
                "site": "http://www.platzi.com",
                "payment_card": "5579099012702512"
            }
        }



class Location(BaseModel):
    city: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    state: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    country: str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    
    class Config:
        schema_extra = {
            "example": {
                "city": "Puebla",
                "state": "Puebla",
                "country": "Mexico"
            }
        }

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
    name: Optional[str] = Query(
        None, 
        min_length = 1, 
        max_length = 50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters."
        ),
    age: int = Query(
        ..., 
        ge = 18,
        title="Person Age",
        description="This is the person age. It's required."
        )      
):
    return {name: age}

# Validation: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt = 0,
        title = "Person ID",
        description = "This is the person ID. It's required."
        )
):
    return {person_id: "It exists"}

# Validation: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        description = "This is the person ID",
        gt = 0
    ),
    person: Person = Body (...),
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    return result

@app.post("/developer/new")
def create_dev(developer: Developer = Body(...)):
    return developer
