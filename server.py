from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import threading
import os
import time

app = Flask(__name__)
CORS(app)

logs = []

# Simple filename-based threat detection
def simple_threat_check(filename):
    keywords = ["virus", "hack", "trojan", "malware", "attack", "worm", "danger"]
    for word in keywords:
        if word in filename.lower():
            return True
    return False

def monitor_folder(folder_path):
    global logs
    logs.append(f"🔍 Started monitoring: {folder_path}")
    while True:
        try:
            for file in os.listdir(folder_path):
                logs.append(f"🟡 Scanning: {file}")
                time.sleep(1)
                if simple_threat_check(file):
                    logs.append(f"🔴 THREAT DETECTED in {file}")
                else:
                    logs.append(f"🟢 Safe: {file}")
            time.sleep(2)
        except Exception as e:
            logs.append(f"⚠ ERROR: {str(e)}")
            time.sleep(2)

@app.route("/start", methods=["POST"])
def start_monitor():
    data = request.get_json()
    folder_path = data.get("folder_path")
    thread = threading.Thread(target=monitor_folder, args=(folder_path,))
    thread.daemon = True
    thread.start()
    return jsonify({"status": "Monitoring Started"})

@app.route("/stream")
def stream_logs():
    def event_stream():
        global logs
        last = 0
        while True:
            while last < len(logs):
                yield f"data: {logs[last]}\n\n"
                last += 1
            time.sleep(1)
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    print("🔥 Server running at: http://127.0.0.1:5000")
    app.run(debug=True)
