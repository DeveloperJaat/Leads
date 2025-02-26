from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ✅ Google Search API Key & Search Engine ID
GOOGLE_SEARCH_API_KEY = "AIzaSyBMFL8kL6li79HITDgVhww3sp6V8ko52No"  # Replace with your actual API key
SEARCH_ENGINE_ID = "7603a783722314f9e"  # Replace with your actual Search Engine ID

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        business_name = request.form["business_name"]
        domain_extension = request.form["domain_extension"]
        location = request.form["location"]

        query = f'{business_name} site:{domain_extension} "{location}"'
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&num=100"

        response = requests.get(url)
        results = response.json()

        return render_template("index.html", results=results.get("items", []))

    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
