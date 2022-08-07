import json

def load_db() -> dict:
    """*.json files only"""
    with open("usersinfo.json", "r", encoding="utf-8") as database:
        db = json.load(database)
    return db

def upload_db(db: dict) -> None:
    with open("usersinfo.json", "w", encoding="utf-8") as database:
        json.dump(db, database, indent=2, ensure_ascii=False)

def reg_user(user_id: str, username: str) -> dict:
    """reg user and imports db"""
    db = load_db()
    if not user_id in db["users"] and not username is None:
        db["users"][user_id] = {"username": username, "packs": [], "language": "en", "status": None}
        db["username_to_id"][username] = user_id
    return db

PM = lambda message: message.chat.type == "private"