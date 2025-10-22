import json

def set_admin_message():
    msg = input("Admin-Nachricht eingeben (leer = löschen): ")
    with open("database.json", "r", encoding="utf-8") as f:
        db = json.load(f)

    db["AdminMessage"] = msg

    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

    print("Admin-Nachricht aktualisiert.")

if __name__ == "__main__":
    set_admin_message()