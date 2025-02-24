from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEYS = ["YOUR_API_KEY_1", "YOUR_API_KEY_2"]  # Add multiple API keys for rotation
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search_google():
    data = request.json
    query = f'"{data["business"]}" "{data["domain"]}" "{data["location"]}"'
    
    for api_key in API_KEYS:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return jsonify(response.json())
    
    return jsonify({"error": "API limit exceeded or invalid request"}), 400

if __name__ == "__main__":
    app.run(debug=True)
