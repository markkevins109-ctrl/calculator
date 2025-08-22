from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Your Groq API key (keep private)
GROQ_API_KEY = "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"
MODEL = "llama3-8b-8192"


# -------------------------
# ADDITION ENDPOINT
# -------------------------
class Numbers(BaseModel):
    a: int
    b: int

@app.post("/add")
def add_numbers(numbers: Numbers):
    return {"result": numbers.a + numbers.b}


# -------------------------
# CHATBOT ENDPOINT
# -------------------------
@app.get("/chat")
def chat(q: str = None):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query parameter ?q=")

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful chatbot."},
                    {"role": "user", "content": q},
                ],
                "max_tokens": 150,
                "temperature": 0.7,
            },
        )

        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return {"question": q, "answer": data["choices"][0]["message"]["content"]}
        else:
            return {"error": "Invalid response from Groq", "details": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
