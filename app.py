from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS für alle erlaubt
DB_FILE = "database.json"

# --- Hilfsfunktionen ---
def load_db():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_ranking():
    db = load_db()
    names = {x["Gruppe"]: x["Anzeigename"] for x in db["AnzeigenahmenG"]}
    ranking = {g: 0 for g in names}

    for round_name, games in db.items():
        if not round_name.startswith("Round"):
            continue
        for g in games:
            if g["winner"]:
                ranking[g["winner"]] += 1

    ranking_list = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    ranking_list = [(names[g], wins) for g, wins in ranking_list]
    return ranking_list

# --- Routen ---
@app.route("/")
def index():
    db = load_db()
    groups = [(g["Gruppe"], g["Anzeigename"]) for g in db["AnzeigenahmenG"]]
    stations = [(s["Station"], s["Anzeigename"]) for s in db.get("AnzeigenahmenS", [])]
    return render_template("index.html", groups=groups, stations=stations)

@app.route("/station/<station>")
def station_page(station):
    db = load_db()
    rounds = []
    names = {x["Gruppe"]: x["Anzeigename"] for x in db["AnzeigenahmenG"]}

    for round_name, games in db.items():
        if not round_name.startswith("Round"):
            continue
        match = next((g for g in games if g["Station"] == station), None)
        if match:
            rounds.append({
                "round": round_name,
                "match": match,
                "f1": names.get(match["fighter1"], match["fighter1"]),
                "f2": names.get(match["fighter2"], match["fighter2"]),
            })

    if not rounds:
        return f"Keine Daten für Station {station}", 404

    return render_template("station.html", rounds=rounds, station=station)

@app.route("/update_winner", methods=["POST"])
def update_winner():
    data = request.json
    station = data["station"]
    round_name = data["round"]
    winner = data["winner"]

    db = load_db()
    games = db[round_name]

    for g in games:
        if g["Station"] == station:
            g["winner"] = winner
            g["finished"] = "1" if winner else "0"
            break

    save_db(db)
    # Broadcast via Socket.IO an alle Clients
    socketio.emit("update")
    return jsonify(success=True)

@app.route("/ranking")
def ranking_page():
    ranking = calculate_ranking()
    return render_template("ranking.html", ranking=ranking)

@app.route("/ranking_data")
def ranking_data():
    return jsonify(calculate_ranking())

@app.route("/group/<group_id>")
def group_page(group_id):
    db = load_db()
    group_names = {x["Gruppe"]: x["Anzeigename"] for x in db["AnzeigenahmenG"]}
    station_names = {x["Station"]: x["Anzeigename"] for x in db["AnzeigenahmenS"]}

    group_name = group_names.get(group_id, group_id)
    history = []

    for round_name, games in db.items():
        if not round_name.startswith("Round"):
            continue
        for g in games:
            if g["fighter1"] == group_id or g["fighter2"] == group_id:
                opponent = g["fighter2"] if g["fighter1"] == group_id else g["fighter1"]
                opponent_name = group_names.get(opponent, opponent)
                station_name = station_names.get(g["Station"], g["Station"])

                status = "offen"
                if g["finished"] == "1":
                    if g["winner"] == group_id:
                        status = "gewonnen ✅"
                    elif g["winner"] == opponent:
                        status = "verloren ❌"
                    else:
                        status = "unentschieden"

                history.append({
                    "station": station_name,
                    "opponent": opponent_name,
                    "status": status
                })

    return render_template("group.html", group_name=group_name, history=history)

# --- Socket.IO Events ---
@socketio.on('connect')
def on_connect():
    print("Client verbunden")

# --- Start ---
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
