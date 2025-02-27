import requests
import os

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def google_search(query, num_results=50):
    results = []
    start = 1  # पहला पेज

    while len(results) < num_results:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&start={start}"

        response = requests.get(url)
        data = response.json()

        if "items" in data:
            results.extend(data["items"])

        start += 10  # अगले पेज के लिए start बढ़ाओ
        if len(data.get("items", [])) < 10:  
            break  # अगर अगले पेज में और डेटा नहीं है तो रुक जाओ

    return results[:num_results]  # जितने रिज़ल्ट मांगे थे, उतने ही दो
