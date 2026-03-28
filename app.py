from flask import Flask, jsonify, send_file, request
import json
import uuid
import os

app = Flask(__name__)

# ------------------------
# 📦 Работа с JSON
# ------------------------

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ------------------------
# 🌐 Роуты
# ------------------------

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/pets")
def pets():
    return jsonify(load_json("pets.json"))

@app.route("/save_trade", methods=["POST"])
def save_trade():
    data = request.json
    trades = load_json("trades.json")

    trade = {
        "id": str(uuid.uuid4()),
        "left": data.get("left", []),
        "right": data.get("right", []),
        "score": data.get("score", 0)
    }

    trades.append(trade)
    save_json("trades.json", trades)

    return jsonify({"id": trade["id"]})

@app.route("/top_trades")
def top_trades():
    trades = load_json("trades.json")
    trades.sort(key=lambda x: x.get("score", 0), reverse=True)
    return jsonify(trades[:10])

# ------------------------
# 🚀 ЗАПУСК (БЕЗ ПАРСЕРА)
# ------------------------

if __name__ == "__main__":
    print("🚀 Сервер запускается...")

    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Порт: {port}")

    app.run(host="0.0.0.0", port=port)
