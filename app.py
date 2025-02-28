from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Environment Variables से API Key और Search Engine ID एक्सेस करना
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")  # Koyeb में सेट करें
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  # Koyeb में सेट करें

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}"

    response = requests.get(url)
    results = response.json()

    return jsonify({"results": results.get("items", [])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
