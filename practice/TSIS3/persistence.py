import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"


def load_json(filename, default):
    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        return default


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def get_settings():
    default = {
        "sound": True,
        "car_color": "Red",
        "difficulty": "Medium"
    }

    return load_json(SETTINGS_FILE, default)


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def get_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def save_score(name, score, distance, coins):
    leaderboard = get_leaderboard()

    leaderboard.append({
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    leaderboard = sorted(
        leaderboard,
        key=lambda x: x["score"],
        reverse=True
    )[:10]

    save_json(LEADERBOARD_FILE, leaderboard)