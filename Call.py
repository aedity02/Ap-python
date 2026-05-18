import os
from google import genai

# Safely fetch the API key hidden inside your Render Environment Settings
GEMINI_KEY = os.environ.get("AIzaSyAWRHqhktuYTA4aMibFMsLxzS7Z81odxGM")

# Initialize the modern, secure GenAI Client
client = genai.Client(api_key=GEMINI_KEY)

def test_ai_screener():
    print("[SYSTEM] Contacting Gemini Core via Unified SDK...")
    
    prompt = (
        "You are an AI assistant. Summarize this fake phone call transcript "
        "in one short line: 'Hey Ae, I am outside your gate with your food delivery.'"
    )
    
    # Correct method using the standard gemini-2.5-flash model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    print("\n--- AI RESPONSE ---")
    print(response.text)

if __name__ == "__main__":
    if not GEMINI_KEY:
        print("[ERROR] GEMINI_API_KEY variable is missing! Check your environment config.")
    else:
        test_ai_screener()
