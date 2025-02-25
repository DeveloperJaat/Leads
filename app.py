import requests
import json
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# List of 7 API keys and their corresponding Search Engine IDs
API_KEYS = [
    {"api_key": "YOUR_API_KEY_1", "cx": "YOUR_SEARCH_ENGINE_ID_1"},
    {"api_key": "YOUR_API_KEY_2", "cx": "YOUR_SEARCH_ENGINE_ID_2"},
    {"api_key": "YOUR_API_KEY_3", "cx": "YOUR_SEARCH_ENGINE_ID_3"},
    {"api_key": "YOUR_API_KEY_4", "cx": "YOUR_SEARCH_ENGINE_ID_4"},
    {"api_key": "YOUR_API_KEY_5", "cx": "YOUR_SEARCH_ENGINE_ID_5"},
    {"api_key": "YOUR_API_KEY_6", "cx": "YOUR_SEARCH_ENGINE_ID_6"},
    {"api_key": "YOUR_API_KEY_7", "cx": "YOUR_SEARCH_ENGINE_ID_7"},
]

# Function to fetch search results using rotating API keys
def fetch_results(query, start_index):
    api_info = API_KEYS[start_index % len(API_KEYS)]
    api_key = api_info["api_key"]
    cx = api_info["cx"]
    
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Extract and filter useful lead data
def extract_leads(data):
    leads = []
    for item in data.get("items", []):
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")

        # Simulate extracting emails (replace with real email extraction logic)
        email = "example@example.com" if "contact" in snippet.lower() else ""

        if email:
            first_name, last_name = title.split(" ")[0], title.split(" ")[-1]
            leads.append({"First Name": first_name, "Last Name": last_name, "Email": email, "Website": link})
    
    return leads

@app.route('/scrape', methods=['GET'])
def scrape():
    query = request.args.get("query")
    total_results = 600
    results_per_request = 90
    all_leads = []

    for i in range(0, total_results, results_per_request):
        data = fetch_results(query, i // results_per_request)
        if data:
            leads = extract_leads(data)
            all_leads.extend(leads)

    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(all_leads)
    df.to_excel("leads.xlsx", index=False)

    return jsonify({"message": "Scraping complete", "total_leads": len(all_leads)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    
