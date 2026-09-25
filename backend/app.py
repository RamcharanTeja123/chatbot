from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Serve frontend
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


# Chat API
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({
            "reply": "Please enter a message."
        }), 400

    # Try Gemini up to 3 times
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=message
            )

            return jsonify({
                "reply": response.text
            })

        except Exception as e:
            print(f"Gemini attempt {attempt + 1} failed:", e)

    return jsonify({
        "reply": "Gemini is temporarily busy. Please try again in a moment."
    }), 503


if __name__ == "__main__":
    app.run(debug=True)