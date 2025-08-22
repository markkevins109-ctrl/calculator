from flask import Flask, request, jsonify, abort
import requests
import os

app = Flask(__name__)

# --- CONFIG ---
# Your custom access key (for users of this API)
API_KEY = "abcd1234"

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")  # <-- put your Groq key here or set in Render
MODEL = "llama3-8b-8192"

# --- Middleware: check API key in URL path ---
@app.before_request
def check_api_key():
    if request.path == "/":
        return None

    parts = request.path.strip("/").split("/", 1)
    if not parts or parts[0] != API_KEY:
        abort(403, description="Forbidden: Invalid API key")

    if len(parts) > 1:
        request.environ["PATH_INFO"] = "/" + parts[1]
    else:
        request.environ["PATH_INFO"] = "/"

# --- Home route ---
@app.route("/")
def home():
    return "✅ Groq Chatbot API is running! Use /<API_KEY>/chat?q=your_question"

# --- Chat endpoint ---
@app.route("/chat")
def chat():
    question = request.args.get("q")
    if not question:
        return jsonify({"error": "Missing question (q) parameter"}), 400

    try:
        # Call Groq LLM API
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful chatbot."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
        )

        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            answer = data["choices"][0]["message"]["content"]
            return jsonify({"question": question, "answer": answer})
        else:
            return jsonify({"error": "Invalid response from Groq API", "details": data}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Run locally ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
