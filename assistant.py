from flask import Flask, request, render_template, redirect, jsonify
import requests, re, webbrowser

# ================= CONFIG =================
PASSWORD = "decken"  # Change your password here

DECKEN_API_KEY = "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"
DECKEN_API_URL = "https://openrouter.ai/api/v1/chat/completions"

WEB_APPS = {
    "gmail": "https://mail.google.com/",
    "facebook": "https://www.facebook.com/",
    "instagram": "https://www.instagram.com/",
    "twitter": "https://twitter.com/",
    "whatsapp": "https://web.whatsapp.com/",
    "youtube": "https://www.youtube.com/",
    "google": "https://www.google.com/"
}

app = Flask(__name__)
logged_in_users = set()

# ================= CLEANER =================
def clean_response(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"^\s*[-•]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n+", "\n", text).strip()
    return text

# ================= DECKEN =================
def ask_decken(prompt):
    headers = {
        "Authorization": f"Bearer {DECKEN_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Decken AI Remote"
    }
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(DECKEN_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            raw_text = response.json()["choices"][0]["message"]["content"]
            return clean_response(raw_text)
        else:
            return f"Decken Error: {response.text}"
    except Exception as e:
        return f"Decken Exception: {e}"

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def home():
    user = request.remote_addr
    if user in logged_in_users:
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.remote_addr
    pw = request.form.get("password")
    if pw == PASSWORD:
        logged_in_users.add(user)
        return redirect("/")
    else:
        return "Incorrect password!"

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    message = data.get("message", "").strip()
    lower_msg = message.lower()

    # Check web apps
    if lower_msg in WEB_APPS:
        webbrowser.open(WEB_APPS[lower_msg])
        reply = f"Opening website: {lower_msg}"
    else:
        reply = ask_decken(message)
        reply = f"🤖 Decken says:\n{reply}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
