from flask import Flask, jsonify, send_file, request
import json, uuid, os, threading, asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from bot import dp, bot
import parser

# Для AI-анализа скринов
import cv2
import pytesseract

app = Flask(__name__)

# --------------------------
# Работа с JSON
# --------------------------
def load_json(file):
    try:
        with open(file,"r") as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file,"w") as f:
        json.dump(data,f,indent=2)

# --------------------------
# API роуты
# --------------------------
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
        "left": data.get("left",[]),
        "right": data.get("right",[]),
        "score": data.get("score",0)
    }
    trades.append(trade)
    save_json("trades.json", trades)
    return jsonify({"id":trade["id"]})

@app.route("/top_trades")
def top_trades():
    trades = load_json("trades.json")
    trades.sort(key=lambda x: x.get("score",0), reverse=True)
    return jsonify(trades[:10])

# --------------------------
# WFL калькулятор
# --------------------------
def calculate_wfl(left_names, right_names):
    pets = {p["name"]:p["value"] for p in load_json("pets.json")}
    left_val = sum(pets.get(name,0) for name in left_names)
    right_val = sum(pets.get(name,0) for name in right_names)
    diff = right_val - left_val
    if diff > 0.3 * left_val: return "WIN"
    elif diff < -0.3 * left_val: return "LOSE"
    return "FAIR"

@app.route("/calc", methods=["POST"])
def calc():
    data = request.json
    result = calculate_wfl(data.get("left",[]), data.get("right",[]))
    return jsonify({"result":result})

# --------------------------
# AI анализ скриншотов
# --------------------------
def extract_pet_names_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, lang='eng+rus')
    names = [line.strip() for line in text.split("\n") if line.strip()]
    return names

@app.route("/ai_trade", methods=["POST"])
def ai_trade():
    file_left = request.files.get("left")
    file_right = request.files.get("right")
    if not file_left or not file_right:
        return jsonify({"error":"Фотографии обеих сторон обязательны"}),400

    file_left.save("left.png")
    file_right.save("right.png")

    left_names = extract_pet_names_from_image("left.png")
    right_names = extract_pet_names_from_image("right.png")

    pets_data = {p["name"]:p["value"] for p in load_json("pets.json")}
    left_sum = sum(pets_data.get(n,0) for n in left_names)
    right_sum = sum(pets_data.get(n,0) for n in right_names)
    diff = right_sum - left_sum

    advice=""
    if diff > 0:
        advice=f"⚠️ Не соглашайся: {right_sum} против твоих {left_sum}"
    elif diff < 0:
        advice=f"✅ Выгодно: твои {left_sum} против {right_sum}"
    else:
        advice=f"🤝 Сделка Fair: {left_sum} против {right_sum}"

    return jsonify({
        "left_names":left_names,
        "right_names":right_names,
        "left_sum":left_sum,
        "right_sum":right_sum,
        "advice":advice
    })

# --------------------------
# Parser каждые 10 минут
# --------------------------
def run_parser():
    print("🔄 Обновляем pets.json")
    asyncio.run(parser.parse())

scheduler = BackgroundScheduler()
scheduler.add_job(run_parser,"interval",minutes=10)
scheduler.start()
run_parser()

# --------------------------
# Бот в отдельном потоке
# --------------------------
def start_bot():
    asyncio.run(dp.start_polling(bot))

threading.Thread(target=start_bot).start()

# --------------------------
if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
