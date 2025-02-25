from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import requests
import os

app = Flask(__name__)

# Load API Keys & Search Engine IDs
API_KEYS = [
    "AIzaSyBMFL8kL6li79HITDgVhww3sp6V8ko52No", "AIzaSyAlKIjAndVVR1L3UepwqgLXbfNtB8kifm4", 
    "AIzaSyBmWLJN79KCzPMLpx2aKAtLTNMaojY8E9Y", "AIzaSyBW28I3Tin6UhJFE5RxCtZr_oMTfN78JgQ", 
    "AIzaSyBWIyKHZ_qNo3onBt9HmrsoXcWLtgTCH6Q", "AIzaSyB8n5E_VX71tyt9BPur4NwgEdAZr146Ub0", 
    "AIzaSyDTese0HQ3pRhctmXFxB_-8nvlfttrbA00"
]
SEARCH_ENGINE_IDS = [
    "7603a783722314f9e", "03902cb98cf1e4449", "a101f70851bd44bd8", 
    "92ed59afad365451b", "a364d5a15cfca4a91", "e62229679dace4132", "85518902d005249f6"
]

# Function to get leads from Google Search API
def get_leads(query, api_key, search_engine_id):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)
    data = response.json()

    leads = []
    if "items" in data:
        for item in data["items"]:
            lead = {
                "name": item.get("title", ""),
                "email": "",  # Email Extraction Logic Needed
                "website": item.get("link", ""),
                "contact": item.get("snippet", ""),
            }
            leads.append(lead)
    return leads

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        business_type = request.form.get("business_type")
        domain_extension = request.form.get("domain_extension")
        location = request.form.get("location")

        if not business_type or not domain_extension or not location:
            return jsonify({"error": "All fields are required!"}), 400

        query = f"{business_type} site:{domain_extension} {location}"

        all_leads = []
        for i in range(len(API_KEYS)):
            leads = get_leads(query, API_KEYS[i], SEARCH_ENGINE_IDS[i])
            all_leads.extend(leads)

        # Remove leads without email
        all_leads = [lead for lead in all_leads if lead["email"]]

        # Convert to DataFrame
        df = pd.DataFrame(all_leads)
        df.to_excel("leads.xlsx", index=False)

        return jsonify({"message": "Scraping complete", "total_leads": len(all_leads)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    return send_file("leads.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
