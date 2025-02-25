import requests
import json
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# List of 7 API keys and their corresponding Search Engine IDs
API_KEYS = [
    {"api_key": "AIzaSyBMFL8kL6li79HITDgVhww3sp6V8ko52No", "cx": "7603a783722314f9e"},
    {"api_key": "AIzaSyAlKIjAndVVR1L3UepwqgLXbfNtB8kifm4", "cx": "03902cb98cf1e4449"},
    {"api_key": "AIzaSyBmWLJN79KCzPMLpx2aKAtLTNMaojY8E9Y", "cx": "a101f70851bd44bd8"},
    {"api_key": "AIzaSyBW28I3Tin6UhJFE5RxCtZr_oMTfN78JgQ", "cx": "92ed59afad365451b"},
    {"api_key": "AIzaSyBWIyKHZ_qNo3onBt9HmrsoXcWLtgTCH6Q", "cx": "a364d5a15cfca4a91"},
    {"api_key": "AIzaSyB8n5E_VX71tyt9BPur4NwgEdAZr146Ub0", "cx": "e62229679dace4132"},
    {"api_key": "AIzaSyDTese0HQ3pRhctmXFxB_-8nvlfttrbA00", "cx": "85518902d005249f6"},
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
    
