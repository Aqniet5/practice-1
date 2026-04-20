import json
import os

def load_data(file, default):
    if not os.path.exists(file):
        with open(file, 'w') as f: json.dump(default, f)
        return default
    try:
        with open(file, 'r') as f: return json.load(f)
    except: return default

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score):
    scores = load_data('leaderboard.json', [])
    scores.append({"name": name, "score": int(score)})
    # Sort and keep top 10
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
    save_data('leaderboard.json', scores)