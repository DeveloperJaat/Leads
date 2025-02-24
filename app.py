import os
import random
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ✅ List of Google Search API keys to rotate requests
API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2",
    "YOUR_API_KEY_3",
    "YOUR_API_KEY_4",
    "YOUR_API_KEY_5",
    "YOUR_API_KEY_6",
    "YOUR_API_KEY_7",
]

# ✅ Search Engine ID (Replace with yours)
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

def get_random_api_key():
    """Randomly selects an API key from the list to distribute the load."""
    return random.choice(API_KEYS)

def google_search(query):
    """Fetch search results from Google API."""
    api_key = get_random_api_key()
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={SEARCH_ENGINE_ID}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        return results
    return []

@app.route("/", methods=["GET"])
def home():
    """Render the home page."""
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    """Handle search requests from frontend."""
    query = request.form.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = google_search(query)
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
