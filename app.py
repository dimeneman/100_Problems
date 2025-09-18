from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'problems.json'

# Load problems from JSON
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        problems = json.load(f)
else:
    # Minimal fallback (replace with your full 100-problem JSON if needed)
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


@app.route('/')
def index():
    # serve static template (no Jinja variables inside)
    return render_template('index.html')


@app.route('/data')
def data():
    progress = calc_progress(problems)
    return jsonify({"problems": problems, "progress": progress})


@app.route('/update', methods=['POST'])
def update():
    # Accept both form-encoded and JSON bodies
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

    # Save updated status
    with open(DATA_FILE, 'w') as f:
        json.dump(problems, f, indent=4)

    progress = calc_progress(problems)
    return jsonify(success=True, progress=progress)


if __name__ == '__main__':
    # debug True for local development
    app.run(debug=True)


