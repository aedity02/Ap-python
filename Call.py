import google.generativeai as genai

# Configure your free Gemini API key
genai.configure(api_key="AIzaSyAWRHqhktuYTA4aMibFMsLxzS7Z81odxGM")

def test_ai_screener():
    print("[SYSTEM] Contacting Gemini Core...")
    
    # Using the fast, efficient flash model
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = (
        "You are an AI assistant. Summarize this fake phone call transcript "
        "in one short line: 'Hey Ae, I am outside your gate with your food delivery.'"
    )
    
    response = model.generate_content(prompt)
    print("\n--- AI RESPONSE ---")
    print(response.text)

if __name__ == "__main__":
    test_ai_screener()
