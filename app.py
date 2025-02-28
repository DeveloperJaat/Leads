from flask import Flask, render_template, request, jsonify
import requests
import os
import re  # ✅ Emails को extract करने के लिए

app = Flask(__name__)

# ✅ Environment Variables से API Key और Search Engine ID एक्सेस करना
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")  # Koyeb में सेट करें
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  # Koyeb में सेट करें

# ✅ Email Extract करने का function
def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)

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
    results = response.json().get("items", [])

    filtered_results = []
    for item in results:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")

        emails = extract_emails(snippet)
        if emails:
            filtered_results.append({
                "title": title,
                "link": link,
                "emails": emails
            })

    return jsonify({"results": filtered_results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
