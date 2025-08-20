from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    a: int
    b: int

@app.post("/add")
def add_numbers(numbers: Numbers):
    return {"result": numbers.a + numbers.b}
