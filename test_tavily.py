from tavily import TavilyClient

API_KEY = "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"  # Replace with the correct key
client = TavilyClient(api_key=API_KEY)

try:
    response = client.search(query="latest AI research")
    print("API Test Response:", response)
except Exception as e:
    print("API Error:", e)
