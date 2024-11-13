import os
import requests
import base64

# Configuration

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OAI_DEPLOYMENT_NAME")


IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_API_KEY,
}

# Payload for the request
payload = {
    "messages": [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant that helps people find information."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Tell me about  india in 3 lines "
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "India is a diverse and culturally rich country located in South Asia, known for its historical heritage, vibrant traditions, and rapid economic growth. It is the world's second-most populous nation and the largest democracy. India features a wide array of landscapes, from the Himalayan peaks to the Indian Ocean coastline."
                }
            ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
}

ENDPOINT = "https://team-2-oai.openai.azure.com/openai/deployments/gpt-4-deploy/chat/completions?api-version=2024-02-15-preview"

# Send request
try:
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    response.raise_for_status()
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
print(response.json())
