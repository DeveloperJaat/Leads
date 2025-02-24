from flask import Flask, request, jsonify, render_template
import requests
import random

app = Flask(__name__)

# List of multiple API keys
API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2",
    "YOUR_API_KEY_3",
    "YOUR_API_KEY_4",
    "YOUR_API_KEY_5",
    "YOUR_API_KEY_6",
    "YOUR_API_KEY_7",
]

CX = "YOUR_CX_CODE"  # Your Google Custom Search Engine ID

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    api_key = random.choice(API_KEYS)  # Select a random API key
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={CX}"
    
    response = requests.get(url)
    data = response.json()

    results = []
    if "items" in data:
        for item in data["items"]:
            results.append({"title": item["title"], "link": item["link"]})

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
