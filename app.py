from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session handling

# 🔥 Initialize Firebase Admin
cred = credentials.Certificate("codeforces-tracker-ee9df-firebase-adminsdk-fbsvc-9404a9c086.json")
firebase_admin.initialize_app(cred)

DATA_FILE = 'problems.json'

# Load problems from JSON
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        problems = json.load(f)
else:
    problems = [
        {"name": "Team", "rating": 800, "link": "https://codeforces.com/problemset/problem/231/A", "completed": False},
        {"name": "Is your horseshoe on the other hoof?", "rating": 800, "link": "https://codeforces.com/problemset/problem/228/A", "completed": False},
        {"name": "Bit++", "rating": 800, "link": "https://codeforces.com/problemset/problem/282/A", "completed": False}
    ]
    with open(DATA_FILE, 'w') as f:
        json.dump(problems, f, indent=4)


def calc_progress(probs):
    total = len(probs)
    if total == 0:
        return 0
    done = sum(1 for p in probs if p.get('completed'))
    return int((done / total) * 100)


# 🔹 Default route → Login first
@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("tracker"))
    return render_template("login.html")


# 🔹 Verify Firebase ID token
@app.route('/verify_token', methods=['POST'])
def verify_token():
    try:
        token = request.json.get("idToken")
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]

        # Save user in session
        session["user"] = uid
        return jsonify({"success": True, "uid": uid})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 401


# 🔹 Tracker page (only if logged in)
@app.route('/tracker')
def tracker():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("tracker.html")


# 🔹 Problems API (protected)
@app.route('/data')
def data():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    progress = calc_progress(problems)
    return jsonify({"problems": problems, "progress": progress})


# 🔹 Update API (protected)
@app.route('/update', methods=['POST'])
def update():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if request.is_json:
        payload = request.get_json()
        problem_name = payload.get('name')
        status = payload.get('completed') is True
    else:
        problem_name = request.form.get('name')
        status = request.form.get('completed') == 'true'

    for problem in problems:
        if problem['name'] == problem_name:
            problem['completed'] = status
            break

    with open(DATA_FILE, 'w') as f:
        json.dump(problems, f, indent=4)

    progress = calc_progress(problems)
    return jsonify(success=True, progress=progress)


# 🔹 Logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
