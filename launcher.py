import subprocess
import webbrowser
import time

def start_system():
    print("🚀 Initializing Sentix Pulse AI...")
    # Start the streamlit server in the background
    subprocess.Popen(["streamlit", "run", "app.py"])
    
    # Give the AI model time to load (important for first run)
    print("⏳ Loading AI Models... (Please wait 5-10 seconds)")
    time.sleep(8)
    
    # Automatically open the browser
    webbrowser.open("http://localhost:8501")
    print("✅ System is LIVE at http://localhost:8501")

if __name__ == "__main__":
    start_system()