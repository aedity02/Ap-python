import os
import subprocess
import sys

# --- AUTOMATIC REQUIREMENT FORCE-INSTALLER ---
# This ensures Render downloads all necessary packages without a requirements.txt file
REQUIRED_PACKAGES = ["flask", "google-genai", "gunicorn"]

for package in REQUIRED_PACKAGES:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"[SYSTEM] Package missing. Deploying auto-installer for: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# --- APP APPLICATION DEPLOYMENT ---
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Safely fetch your API key from Render's Environment Variable Panel
GEMINI_KEY = os.environ.get("GAIzaSyAWRHqhktuYTA4aMibFMsLxzS7Z81odxGM")

# Local memory to buffer the log history for Sketchware requests
call_logs = []

SYSTEM_INSTRUCTION = """
You are an AI receptionist screening phone calls for Ae Singh.
Analyze the provided transcript of the caller.
If the call is an emergency, an important business inquiry, or a delivery driver outside, respond with exactly: FORWARD.
If the call is a telemarketer, spam, automated bot, or low-priority chatter, respond with exactly: BLOCK.
"""

@app.route('/')
def home():
    return jsonify({"status": "AI Call Screener Active", "secure": True})

@app.route('/screen_call', methods=['POST'])
def screen_call():
    # Verify environment key configuration
    if not GEMINI_KEY:
        return jsonify({"error": "Server configuration error: Missing GEMINI_API_KEY environment variable"}), 500

    data = request.get_json()
    if not data or 'transcript' not in data:
        return jsonify({"error": "Missing transcript payload"}), 400
    
    caller_name = data.get('caller', 'UNKNOWN')
    transcript = data.get('transcript', '')
    
    try:
        # Connect safely using the modern unified GenAI Client
        client = genai.Client(api_key=GEMINI_KEY)
        
        # Analyze using standard flash model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Caller: {caller_name}\nTranscript: {transcript}\n\nDecision Rules: {SYSTEM_INSTRUCTION}"
        )
        decision = response.text.strip().upper()
        
        log_entry = {
            "timestamp": os.popen('date +"%H:%M:%S"').read().strip(),
            "caller": caller_name,
            "transcript": transcript,
            "action": "FORWARDED" if "FORWARD" in decision else "BLOCKED"
        }
        call_logs.append(log_entry)
        
        return jsonify({
            "decision": log_entry["action"],
            "payload": log_entry
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for your Sketchware User Interface to pull down live data streams
@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": call_logs[::-1]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
