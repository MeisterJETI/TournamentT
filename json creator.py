import json

# daten = {
    # "gruppen": [
        # {"ID": "1", "name": "Gruppe 1", "wins": 0, "looses": 0, "progress": "000000"},
        # {"ID": "2", "name": "Gruppe 2", "wins": 0, "looses": 0, "progress": "000000"},
        # {"ID": "3", "name": "Gruppe 3", "wins": 0, "looses": 0, "progress": "000000"},
        # {"ID": "4", "name": "Gruppe 4", "wins": 0, "looses": 0, "progress": "000000"},
        # {"ID": "5", "name": "Gruppe 5", "wins": 0, "looses": 0, "progress": "000000"},
        # {"ID": "6", "name": "Gruppe 6", "wins": 0, "looses": 0, "progress": "000000"}
        # #progress: 0=not, 1=waiting for match, 2=battle, 3=finished
    # ],
    # "stationen": [
        # {"ID": "1", "state": "free", "name": "Mattenberg"},
        # {"ID": "2", "state": "free", "name": "Parkour"},
        # {"ID": "3", "state": "free", "name": "Zeitfangen"},
        # {"ID": "4", "state": "free", "name": "Voelkerball"},
        # {"ID": "5", "state": "free", "name": "Kreativ"},
        # {"ID": "6", "state": "free", "name": "Schwammlauf"}
        # #state: free, busy, que
    # ]
# }

daten = {
    "Round 1": [
        {"ID": "game 1", "Station": "S1", "fighter1": "G1", "fighter2": "G7", "finished": "0", "winner": ""},
        {"ID": "game 2", "Station": "S2", "fighter1": "G2", "fighter2": "G8", "finished": "0", "winner": ""},
        {"ID": "game 3", "Station": "S3", "fighter1": "G3", "fighter2": "G9", "finished": "0", "winner": ""},
        {"ID": "game 4", "Station": "S4", "fighter1": "G4", "fighter2": "G10", "finished": "0", "winner": ""},
        {"ID": "game 5", "Station": "S5", "fighter1": "G5", "fighter2": "G11", "finished": "0", "winner": ""},
        {"ID": "game 6", "Station": "S6", "fighter1": "G6", "fighter2": "G12", "finished": "0", "winner": ""}
    ],
    "Round 2": [
        {"ID": "game 1", "Station": "S1", "fighter1": "G6", "fighter2": "G8", "finished": "0", "winner": ""},
        {"ID": "game 2", "Station": "S2", "fighter1": "G1", "fighter2": "G9", "finished": "0", "winner": ""},
        {"ID": "game 3", "Station": "S3", "fighter1": "G2", "fighter2": "G10", "finished": "0", "winner": ""},
        {"ID": "game 4", "Station": "S4", "fighter1": "G3", "fighter2": "G11", "finished": "0", "winner": ""},
        {"ID": "game 5", "Station": "S5", "fighter1": "G4", "fighter2": "G12", "finished": "0", "winner": ""},
        {"ID": "game 6", "Station": "S6", "fighter1": "G5", "fighter2": "G7", "finished": "0", "winner": ""}
    ],
    "Round 3": [
        {"ID": "game 1", "Station": "S1", "fighter1": "G5", "fighter2": "G9", "finished": "0", "winner": ""},
        {"ID": "game 2", "Station": "S2", "fighter1": "G6", "fighter2": "G10", "finished": "0", "winner": ""},
        {"ID": "game 3", "Station": "S3", "fighter1": "G1", "fighter2": "G11", "finished": "0", "winner": ""},
        {"ID": "game 4", "Station": "S4", "fighter1": "G2", "fighter2": "G12", "finished": "0", "winner": ""},
        {"ID": "game 5", "Station": "S5", "fighter1": "G6", "fighter2": "G7", "finished": "0", "winner": ""},
        {"ID": "game 6", "Station": "S6", "fighter1": "G4", "fighter2": "G8", "finished": "0", "winner": ""}
    ],
    "Round 4": [
        {"ID": "game 1", "Station": "S1", "fighter1": "G4", "fighter2": "G10", "finished": "0", "winner": ""},
        {"ID": "game 2", "Station": "S2", "fighter1": "G5", "fighter2": "G11", "finished": "0", "winner": ""},
        {"ID": "game 3", "Station": "S3", "fighter1": "G6", "fighter2": "G12", "finished": "0", "winner": ""},
        {"ID": "game 4", "Station": "S4", "fighter1": "G1", "fighter2": "G7", "finished": "0", "winner": ""},
        {"ID": "game 5", "Station": "S5", "fighter1": "G2", "fighter2": "G8", "finished": "0", "winner": ""},
        {"ID": "game 6", "Station": "S6", "fighter1": "G3", "fighter2": "G9", "finished": "0", "winner": ""}
    ],
    "Round 5": [
        {"ID": "game 1", "Station": "S1", "fighter1": "G3", "fighter2": "G11", "finished": "0", "winner": ""},
        {"ID": "game 2", "Station": "S2", "fighter1": "G4", "fighter2": "G12", "finished": "0", "winner": ""},
        {"ID": "game 3", "Station": "S3", "fighter1": "G5", "fighter2": "G7", "finished": "0", "winner": ""},
        {"ID": "game 4", "Station": "S4", "fighter1": "G6", "fighter2": "G8", "finished": "0", "winner": ""},
        {"ID": "game 5", "Station": "S5", "fighter1": "G1", "fighter2": "G9", "finished": "0", "winner": ""},
        {"ID": "game 6", "Station": "S6", "fighter1": "G2", "fighter2": "G10", "finished": "0", "winner": ""}
    ],
    "Round 6": [
        {"ID": "game 1", "Station": "S1", "fighter1": "G2", "fighter2": "G12", "finished": "0", "winner": ""},
        {"ID": "game 2", "Station": "S2", "fighter1": "G3", "fighter2": "G7", "finished": "0", "winner": ""},
        {"ID": "game 3", "Station": "S3", "fighter1": "G4", "fighter2": "G8", "finished": "0", "winner": ""},
        {"ID": "game 4", "Station": "S4", "fighter1": "G5", "fighter2": "G9", "finished": "0", "winner": ""},
        {"ID": "game 5", "Station": "S5", "fighter1": "G6", "fighter2": "G10", "finished": "0", "winner": ""},
        {"ID": "game 6", "Station": "S6", "fighter1": "G1", "fighter2": "G11", "finished": "0", "winner": ""}
    ],
    "AnzeigenahmenG": [
        {"Gruppe": "G1", "Anzeigename": "Gruppe A"},
        {"Gruppe": "G2", "Anzeigename": "Gruppe B"},
        {"Gruppe": "G3", "Anzeigename": "Gruppe C"},
        {"Gruppe": "G4", "Anzeigename": "Gruppe D"},
        {"Gruppe": "G5", "Anzeigename": "Gruppe E"},
        {"Gruppe": "G6", "Anzeigename": "Gruppe F"},
        {"Gruppe": "G7", "Anzeigename": "Gruppe G"},
        {"Gruppe": "G8", "Anzeigename": "Gruppe H"},
        {"Gruppe": "G9", "Anzeigename": "Gruppe I"},
        {"Gruppe": "G10", "Anzeigename": "Gruppe J"},
        {"Gruppe": "G11", "Anzeigename": "Gruppe K"},
        {"Gruppe": "G12", "Anzeigename": "Gruppe L"}
    ],
    "AnzeigenahmenS": [
        {"Station": "S1", "Anzeigename": "Völkerball"},
        {"Station": "S2", "Anzeigename": "Mattenberg"},
        {"Station": "S3", "Anzeigename": "Zeitfangen"},
        {"Station": "S4", "Anzeigename": "Parkour"},
        {"Station": "S5", "Anzeigename": "Schwammlauf"},
        {"Station": "S6", "Anzeigename": "Kreativ"}
    ]
}

# Speichern
with open("database.json", "w") as f:
    json.dump(daten, f, indent=4)

# Laden
with open("database.json", "r") as f:
    daten_laden = json.load(f)