from flask import Flask, render_template, request, jsonify
import requests
import json
import threading
import time
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lordhozoo2025' 
jarvis_lines = [
    "Hello, Sir. Awaiting your command.",
    "Analyzing TikTok security protocols...",
    "Initiating report sequence...",
    "Report submitted, Sir.",
    "Engaging countermeasures...",
    "System fully operational.",
    "TikTok defenses are weak, Sir.",
    "Executing unlimited report spam...",
    "Do you need assistance, Sir?",
    "The report operation has begun",
    "Target Aquired",
    "Starting attack sir !"

]
def generate_random_id():
    return ''.join(random.choices('abcdef0123456789', k=16))
def report_tiktok(username):
    url = "https://www.tiktok.com/api/review/report/user"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.tiktok.com",
        "Referer": "https://www.tiktok.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Secsdk-Csrf-Token": ""  
    }
    device_id = generate_random_id()
    web_id = generate_random_id()
    data = {
        "aid": 1988,
        "app_language": "id",
        "app_name": "tiktok_web",
        "browser_language": "id",
        "browser_name": "Chrome",
        "browser_version": "58.0.3029.110",
        "device_id": device_id,
        "os": "Linux x86_64",
        "referer": "https://www.tiktok.com/",
        "report_type": "OTHER",
        "reason": "Spam",
        "target_id": username,
        "web_id": web_id
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() 
        try:
            response_json = response.json()
            print(f"Response: {response_json}") #Debug
            if response.status_code == 200:
              return "Akun berhasil dilaporkan" # Return status
            else:
              return "Gagal melaporkan akun" # Return status
        except json.JSONDecodeError:
            print("Response is not in JSON format")
            print(f"Response text: {response.text}") #Debug response
            if response.status_code == 200:
                return "Akun berhasil dilaporkan (response non-JSON)" # Return status
            else:
                return "Gagal melaporkan akun (response non-JSON)" # Return status


    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}" # Return status

# Fungsi untuk spam report (threaded)
def spam_report(username, stop_event):
    while not stop_event.is_set():
        result = report_tiktok(username)
        print(f"Report result: {result}")
        time.sleep(0.1) # Tanpa Delay

# Route untuk halaman utama
@app.route('/', methods=['GET', 'POST'])
def index():
    global spam_thread, stop_event
    if request.method == 'POST':
        username = request.form['username']
        if request.form['action'] == 'start':
            stop_event = threading.Event()
            spam_thread = threading.Thread(target=spam_report, args=(username, stop_event))
            spam_thread.daemon = True # Kill thread on exit
            spam_thread.start()
            return render_template('index.html', username=username, jarvis=random.choice(jarvis_lines),spam_status="Spamming...")
        elif request.form['action'] == 'stop':
            stop_event.set()
            if spam_thread and spam_thread.is_alive():
                spam_thread.join() # Wait for thread to finish
            return render_template('index.html', username=username, jarvis=random.choice(jarvis_lines),spam_status="Spamming Stopped")

    return render_template('index.html', username='', jarvis=random.choice(jarvis_lines),spam_status="")

# Route untuk mendapatkan kalimat JARVIS
@app.route('/jarvis')
def jarvis():
    return jsonify({'line': random.choice(jarvis_lines)})

if __name__ == '__main__':
    app.run(debug=True, port=8080) #Port
