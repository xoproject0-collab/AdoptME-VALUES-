from flask import Flask, jsonify, request
import json, uuid, os, threading, asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from bot import dp, bot
import parser
import cv2, pytesseract

app = Flask(__name__)

def load_json(file):
    try:
        with open(file,"r") as f:
            return json.load(f)
    except:
        return []

def save_json(file,data):
    with open(file,"w") as f:
        json.dump(data,f,indent=2)

# -------------------
@app.route("/pets")
def pets():
    return jsonify(load_json("pets.json"))

@app.route("/calc", methods=["POST"])
def calc():
    data = request.json
    pets_data = {p["name"]:p["value"] for p in load_json("pets.json")}
    left_sum = sum(pets_data.get(n,0) for n in data.get("left",[]))
    right_sum = sum(pets_data.get(n,0) for n in data.get("right",[]))
    diff = right_sum - left_sum
    if diff > 0.3*left_sum: result="WIN"
    elif diff < -0.3*left_sum: result="LOSE"
    else: result="FAIR"
    return jsonify({"result":result,"left_sum":left_sum,"right_sum":right_sum})

# -------------------
# AI анализ фото
def extract_names(image_path):
    img=cv2.imread(image_path)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    text=pytesseract.image_to_string(thresh,lang='eng+rus')
    return [line.strip() for line in text.split("\n") if line.strip()]

@app.route("/ai_trade", methods=["POST"])
def ai_trade():
    f_left=request.files.get("left")
    f_right=request.files.get("right")
    if not f_left or not f_right: return jsonify({"error":"Нужны обе фотографии"}),400
    f_left.save("left.png")
    f_right.save("right.png")
    left_names=extract_names("left.png")
    right_names=extract_names("right.png")
    pets_data={p["name"]:p["value"] for p in load_json("pets.json")}
    left_sum=sum(pets_data.get(n,0) for n in left_names)
    right_sum=sum(pets_data.get(n,0) for n in right_names)
    diff=right_sum-left_sum
    if diff>0: advice=f"⚠️ Не соглашайся: {right_sum} против твоих {left_sum}"
    elif diff<0: advice=f"✅ Выгодно: твои {left_sum} против {right_sum}"
    else: advice=f"🤝 Сделка FAIR: {left_sum} против {right_sum}"
    return jsonify({"left":left_names,"right":right_names,"advice":advice})

# -------------------
# Parser каждые 10 минут
def run_parser(): asyncio.run(parser.parse())
scheduler=BackgroundScheduler()
scheduler.add_job(run_parser,"interval",minutes=10)
scheduler.start()
run_parser()

# -------------------
# Запуск Telegram бота
def start_bot(): asyncio.run(dp.start_polling(bot))
threading.Thread(target=start_bot).start()

# -------------------
if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
