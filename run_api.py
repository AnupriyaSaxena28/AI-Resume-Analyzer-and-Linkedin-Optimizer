
import os
import sys
import threading
import time
from pyngrok import ngrok, conf
from dotenv import load_dotenv
import uvicorn
from api import app

# Load environment variables
load_dotenv()

def run_server():
    """Run the uvicorn server"""
    uvicorn.run(app, host="0.0.0.0", port=8001)

def main():
    print("🚀 Starting AI Resume Analyzer API with Ngrok...")
    
    # 0. Set Auth Token from Environment
    token = os.getenv("NGROK_AUTHTOKEN")
    if token:
        print("🔐 Found NGROK_AUTHTOKEN in environment")
        ngrok.set_auth_token(token)
    else:
        print("⚠️ No NGROK_AUTHTOKEN found. Tunnel might fail if not configured globally.")

    # 1. Start Ngrok Tunnel
    try:
        # Open a HTTP tunnel on port 8001
        public_url = ngrok.connect(8001).public_url
        print(f"\n✅ Public API URL: {public_url}")
        print(f"📄 Docs available at: {public_url}/docs\n")
        
    except Exception as e:
        print(f"\n❌ Ngrok Error: {str(e)}")
        print("💡 Hint: You may need to set your authtoken if you haven't already.")
        print("   Run: ngrok config add-authtoken <YOUR_TOKEN>")
        return

    # 2. Start Uvicorn Server
    print("⏳ Starting Local Server...")
    # We run uvicorn in the main thread to keep the script alive
    # Ngrok runs in a background thread managed by pyngrok
    run_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server and tunnel...")
        sys.exit(0)
