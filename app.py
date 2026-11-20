from flask import Flask, render_template
import subprocess
import platform

app = Flask(__name__)

# Senarai device yang nak monitor
devices = [
    {"name": "Google DNS", "host": "8.8.8.8"},
    {"name": "Cloudflare DNS", "host": "1.1.1.1"},
    {"name": "Local Router", "host": "192.168.1.254"},
    {"name": "Phone Aku", "host": "192.168.1.13"},  # tambah ni
]

def ping(host):
    if platform.system() == "Windows":
        command = ["ping", "-n", "1", "-w", "2000", host]
    else:
        command = ["ping", "-c", "1", "-W", "2", host]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Windows kadang return 0 walaupun fail, so kita check output jugak
    output = result.stdout.decode('utf-8', errors='ignore')
    if platform.system() == "Windows":
        return "TTL=" in output  # kalau ada TTL dalam output = online
    return result.returncode == 0
@app.route('/')
def index():
    results = []
    for device in devices:
        status = ping(device["host"])
        results.append({
            "name": device["name"],
            "host": device["host"],
            "status": "Online" if status else "Offline"
        })
    return render_template('index.html', devices=results)

if __name__ == '__main__':
    app.run(debug=True)