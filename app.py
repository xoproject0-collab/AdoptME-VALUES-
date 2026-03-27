from flask import Flask, jsonify, send_file, request
import json, uuid, asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from parser import parse

app = Flask(__name__)

def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

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
        "left": data["left"],
        "right": data["right"],
        "score": data["score"]
    }

    trades.append(trade)
    save_json("trades.json", trades)

    return jsonify({"id": trade["id"]})

@app.route("/top_trades")
def top_trades():
    trades = load_json("trades.json")
    trades.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(trades[:10])

# 🔥 авто-парсинг каждые 5 минут
def run_parser():
    asyncio.run(parse())

scheduler = BackgroundScheduler()
scheduler.add_job(run_parser, "interval", minutes=5)
scheduler.start()

if __name__ == "__main__":
    run_parser()  # первый запуск
    app.run(host="0.0.0.0", port=10000)