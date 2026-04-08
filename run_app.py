import subprocess
import webbrowser
import time

# Start Streamlit app
process = subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for server to start
time.sleep(3)

# Open browser automatically
webbrowser.open("http://localhost:8501")

# Keep app running
process.wait()