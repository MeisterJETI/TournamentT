from flask import Flask, render_template, request, jsonify, Response
import json, threading

app = Flask(__name__)
DB_FILE = "database.json"

#Hilfsfunktionen
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

    # Liste sortieren (meiste Siege oben)
    ranking_list = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    # Anzeigenamen einsetzen
    ranking_list = [(names[g], wins) for g, wins in ranking_list]
    return ranking_list

#SSE Broadcasting
listeners = []

def event_stream():
    q = threading.Event()
    listeners.append(q)
    try:
        while True:
            q.wait()
            q.clear()
            yield f"data: update\n\n"
    finally:
        listeners.remove(q)

def notify_all():
    for l in listeners:
        l.set()

#Routen
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
    notify_all()
    return jsonify(success=True)

@app.route("/ranking")
def ranking_page():
    ranking = calculate_ranking()
    return render_template("ranking.html", ranking=ranking)

@app.route("/ranking_data")
def ranking_data():
    # Liefert Ranking als JSON für Ajax
    return jsonify(calculate_ranking())

@app.route("/events")
def events():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/group/<group_id>")
def group_page(group_id):
    db = load_db()
    # Anzeigenamen für Gruppen und Stationen
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

@app.route("/get_station_state/<station>")
def get_station_state(station):
    db = load_db()
    state = {}
    for round_name in [f"Round {i}" for i in range(1,7)]:
        for game in db[round_name]:
            if game["Station"] == station:
                state[round_name] = game["winner"]
    return jsonify(state)


@app.route("/")
def index():
    db = load_db()
    # Anzeigenamen für Gruppen
    groups = [(g["Gruppe"], g["Anzeigename"]) for g in db["AnzeigenahmenG"]]
    # Anzeigenamen für Stationen
    stations = [(s["Station"], s["Anzeigename"]) for s in db.get("AnzeigenahmenS", [])]
    return render_template("index.html", groups=groups, stations=stations)

import time

@app.route("/start_timer", methods=["POST"])
def start_timer():
    data = request.get_json()
    station = data["station"]
    minutes = int(data.get("minutes", 0))
    seconds = int(data.get("seconds", 0))
    duration = minutes * 60 + seconds

    db = load_db()
    if "Timers" not in db:
        db["Timers"] = {}

    db["Timers"][station] = {
        "duration": duration,
        "start_time": time.time(),
        "running": True
    }
    save_db(db)

    return jsonify(success=True)


@app.route("/get_timer/<station>")
def get_timer(station):
    db = load_db()
    timers = db.get("Timers", {})
    timer = timers.get(station)

    if not timer or not timer.get("running", False):
        return jsonify(remaining=0, running=False)

    # Sicherheitsprüfung: start_time und duration existieren
    start_time = timer.get("start_time")
    duration = timer.get("duration", 0)

    if start_time is None:
        return jsonify(remaining=0, running=False)

    elapsed = int(time.time() - start_time)
    remaining = max(0, duration - elapsed)

    # Timer automatisch stoppen, wenn fertig
    if remaining == 0:
        timer["running"] = False
        save_db(db)

    return jsonify(remaining=remaining, running=timer["running"])

@app.route("/reset_timer", methods=["POST"])
def reset_timer():
    data = request.get_json()
    station = data["station"]

    db = load_db()
    if "Timers" in db and station in db["Timers"]:
        db["Timers"][station]["running"] = False
        db["Timers"][station]["duration"] = 0
        db["Timers"][station]["start_time"] = None
        save_db(db)

    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0")
