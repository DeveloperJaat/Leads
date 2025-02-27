from flask import Flask, render_template, request
import requests
import os  # ✅ Environment Variables पढ़ने के लिए

app = Flask(__name__)

# ✅ Environment Variables से API Key और Search Engine ID एक्सेस करना
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")  # Koyeb में सेट करें
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  # Koyeb में सेट करें

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        business_name = request.form["business_name"]
        domain_extension = request.form["domain_extension"]
        location = request.form["location"]

        query = f'"{business_name}" "{domain_extension}" "{location}"'
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&num=100"

        response = requests.get(url)
        results = response.json()

        return render_template("index.html", results=results.get("items", []))

    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
